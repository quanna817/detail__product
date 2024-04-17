from fastapi.middleware.cors import CORSMiddleware  
from fastapi import FastAPI, HTTPException, Depends, Header, Security
from sqlalchemy.orm import Session, relationship
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

# Define your SQLAlchemy model here
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_token_header(token: str = Header(...)):
    if token != "this_token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return token

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(credentials: HTTPBasicCredentials=Security(security)):
    username = credentials.username
    password = credentials.password
    
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    # if not user or not verify_password(password, user.password):
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )
    return user

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    product_id = Column(Integer, ForeignKey('products.id'))

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)

    # Define the relationship with images
    images = relationship("Image", backref="product")
    price_history = relationship("PriceHistory", backref="product")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Ensure our database schema is created
Base.metadata.create_all(bind=engine)

# Pydantic model for the image
class ImageResponse(BaseModel):
    id: int
    url: str

# Modify the ProductResponse model to include images
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    images: List[ImageResponse]


class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: datetime

# Modify the endpoints to handle images
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductResponse, db: Session = Depends(get_db), token: str = Depends(get_token_header), current_user: User = Depends(get_current_user)):
    db_product = Product(**product.dict(exclude={"images"}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    for image_data in product.images:
        db_image = Image(url=image_data.url, product_id=db_product.id)
        db.add(db_image)
    db.commit()
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db), token: str = Depends(get_token_header), current_user: User = Depends(get_current_user)):
    products = db.query(Product).all()
    return [
        ProductResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            images=[ImageResponse(id=image.id, url=image.url) for image in p.images]
        ) for p in products
    ]

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        images=[ImageResponse(id=image.id, url=image.url) for image in product.images]
    )


@app.put("/products/{product_id}/price", response_model=ProductResponse)
async def update_product_price(product_id: int, new_price: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    old_price = product.price
    product.price = new_price
    db.commit()
    # Only add a new price history entry if the price has changed
    if old_price != new_price:
        db_price_history = PriceHistory(product_id=product_id, price=new_price)
        db.add(db_price_history)
        db.commit()
    return product


@app.get("/products/{product_id}/price_history", response_model=List[PriceHistoryResponse])
async def get_product_price_history(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    price_history = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()
    if not price_history:
        raise HTTPException(status_code=404, detail="Price history not found for this product")
    return price_history

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

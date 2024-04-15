from fastapi.middleware.cors import CORSMiddleware  
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, relationship
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from typing import List
from datetime import datetime

# Define your SQLAlchemy model here
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text

app = FastAPI()

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
async def create_product(product: ProductResponse, db: Session = Depends(get_db)):
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
async def get_products(db: Session = Depends(get_db)):
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
async def get_product(product_id: int, db: Session = Depends(get_db)):
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
async def update_product_price(product_id: int, new_price: float, db: Session = Depends(get_db)):
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
async def get_product_price_history(product_id: int, db: Session = Depends(get_db)):
    price_history = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()
    if not price_history:
        raise HTTPException(status_code=404, detail="Price history not found for this product")
    return price_history

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

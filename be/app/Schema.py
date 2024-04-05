from pydantic import BaseModel
from typing import List, Optional

# class CategoryBase(BaseModel):
#     name: str
#     type: str

# class CategoryCreate(CategoryBase):
#     pass


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

# class ProductCreate(ProductBase):
#     pass

# class Image(BaseModel):
#     id: int
#     image_url: str

#     class Config:
#         orm_mode = True

class Product(ProductBase):
    id: int
    # images: List[Image] = []

    class Config:
        orm_mode = True


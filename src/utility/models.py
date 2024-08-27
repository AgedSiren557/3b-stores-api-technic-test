from pydantic import BaseModel, Field
from typing import Optional, List

class ProductsModel(BaseModel):
  id: int = Field(default=None, alias="id")
  sku: str = Field(default=None, alias="sku")
  name: str = Field(default=None, alias="name")
  stock: int = Field(default=100, alias="stock")
  price: Optional[str] = Field(default=None, alias="price")

class OrderProduct(BaseModel):
  id: int = Field(default=None, alias="id")
  sku: str = Field(alias="sku")
  quantity: int = Field(default=None, alias="quantity")
  sub_total: str = Field(default=None, alias="sub_total")
  orders_id: int = Field(default=None, alias="orders_id")
  products_id: int = Field(default=None, alias="products_id")

class OrdersModel(BaseModel):
  id: int = Field(default=None, alias="id")
  order_id: str = Field(default=None, alias="order_id")
  total: str = Field(default="0.00", alias="total")
  products: List[OrderProduct] = Field(default=None, alias="products")

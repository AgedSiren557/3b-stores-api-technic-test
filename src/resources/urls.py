from src.resources.products import Products
from src.resources.orders import Orders
from src.resources.inventories import Inventories


def url_patterns(api):
  api.add_resource(Inventories, "/api/inventories/product/<id_product>")
  api.add_resource(Products, "/api/products")
  api.add_resource(Orders, "/api/orders")
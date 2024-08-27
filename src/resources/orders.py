import json
import sqlite3
import os
from flask import Response, request
from flask_restful import Resource
from src.utility.schemas import orders_schema
from src.utility.decorators import validate_request
from src.services.db import DataBaseService
from src.exceptions import (
  NotItemInInDatabaseException, ItemWithOutPriceException
)
from src.utility.models import (
  ProductsModel, OrdersModel,
  OrderProduct
)


class Orders(Resource):
  @classmethod
  @validate_request(schema = orders_schema)
  def post(cls):
    data = OrdersModel(**request.json)
    
    try:
      db_service = DataBaseService(db_name=os.getenv("DB_CONNECTION"))
      
      #* Validate the existance of products
      for order_products in data.products:
        product = db_service.select(table="products", conditions= {"sku": order_products.sku})
        if len(product) == 0:
          raise NotItemInInDatabaseException()
        
        product_model = ProductsModel(**product[0])
        order_products.products_id = product_model.id
        cls.__validate_price__(product=product_model, order_product=order_products)
        
        data.total = cls.__add_number_strings__(
          first= data.total, 
          second= order_products.sub_total
        )
        
        product_model.stock -= order_products.quantity
        
        db_service.update(
          table="products",
          data={ "stock": product_model.stock},
          conditions={ "id": product_model.id }
        )
        
      #* Create order on db
      column_names = [field.alias for field in data.model_fields.values() if field.alias != "products"]
      values_order = [value for key, value in data.model_dump().items() if key != "products"]
      
      db_service.insert(
        table="orders", 
        columns=column_names, 
        values=values_order
      )
      order = db_service.select(
        table="orders",
        conditions={
          "order_id": data.order_id
        }
      )
      
      #* Get id of order
      order_model = OrdersModel(**order[0])
      for order_product in data.products:
        order_product.orders_id = order_model.id
        columns = [field.alias for field in order_product.model_fields.values() if field.alias != "sku"]
        values = [value for key, value in order_product.model_dump().items() if key != "sku" ]
        
        db_service.insert(
          table="products_orders", 
          columns=columns, 
          values=values
        )
        
    except (
      sqlite3.Error, sqlite3.OperationalError,
      sqlite3.ProgrammingError, sqlite3.IntegrityError,
      ItemWithOutPriceException
    ) as e:
      
      error_response = {
        "error": str(e)
      }
      return Response(json.dumps(error_response), mimetype="application/json", status=400)
    
    except NotItemInInDatabaseException:
      return Response(headers={"x-status-messaage": f"Sku doesnt exist"}, status=204)
    
    finally:
      db_service.close_connection()
      
    return Response(json.dumps({"message":"Succesfull Operation"}), mimetype="application/json", status=201)
  
  
  def __validate_price__(product:ProductsModel, order_product: OrderProduct):
    if product.price is None:
      raise ItemWithOutPriceException(f"Item with sku: {product.sku} has naot price in db")
    order_product.sub_total = str(float(product.price) * order_product.quantity)
    print (order_product.sub_total)
  
  def __add_number_strings__(first: str, second:str)-> str:
    return str(float(first)+float(second))
  
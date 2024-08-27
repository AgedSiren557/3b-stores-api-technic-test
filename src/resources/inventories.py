import json
import sqlite3
import os
from flask import Response, request
from flask_restful import Resource
from src.utility.schemas import inventories_schema
from src.utility.decorators import validate_request
from src.utility.models import ProductsModel
from src.services.db import DataBaseService
from src.exceptions import NotItemInInDatabaseException

class Inventories(Resource):
  @classmethod
  @validate_request(schema = inventories_schema)
  def patch(cls, id_product:str, *args, **kwargs):
    if not id_product.isdigit() :
      return Response(json.dumps({"error":"<id_product> param must be a valid id"}), mimetype="application/json", status=400)
    
    new_stock = request.get_json()["stock"]
    try:
      db_service = DataBaseService(db_name=os.getenv("DB_CONNECTION"))
      products = db_service.select(
        table= "products", 
        conditions={ "id": int(id_product) }
      )
      if len(products) == 0:
        raise NotItemInInDatabaseException()
      
      data = ProductsModel(**products[0])
      data.stock += new_stock
      db_service.update(
        table=  "products",
        data = {"stock": data.stock },
        conditions = {"id": int(id_product)}
      )
      
    except (
      sqlite3.Error,
      sqlite3.OperationalError,
      sqlite3.ProgrammingError,
      sqlite3.IntegrityError
    ) as e:
      error_response = {
        "error": str(e)
      }
      return Response(json.dumps(error_response), mimetype="application/json", status=400)
    
    except NotItemInInDatabaseException:
      return Response(headers={"x-status-messaage": f"Iten with id:{id_product} doesnt exist in database"}, status=204)
    
    finally:
      db_service.close_connection()
      
    return Response(json.dumps({"message":"Succesfull Operation"}), mimetype="application/json", status=200)
import json
import os
import sqlite3
from flask import Response, request
from flask_restful import Resource
from src.utility.schemas import products_schema
from src.utility.decorators import validate_request
from src.services.db import DataBaseService
from src.utility.models import ProductsModel

class Products(Resource):
  @classmethod
  @validate_request(schema = products_schema)
  def post(cls):
    data = ProductsModel(**request.json)
    alias_list = [field.alias for field in data.model_fields.values() if field.alias]
    values = [getattr(data, field.alias) if field.alias else getattr(data, field.name) for field in data.model_fields.values()]
    try:
      db_service = DataBaseService(db_name=os.getenv("DB_CONNECTION"))
      db_service.insert("products", columns=alias_list,values=values)
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
    finally:
      db_service.close_connection()
    return Response(json.dumps({"message":"Succesfull Operation"}), mimetype="application/json", status=201)
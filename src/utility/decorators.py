import json
from jsonschema import validate, ValidationError
from flask import Response, request
from src.utility.schemas import product_id_schema

def validate_request(schema={}):
  def decorator(func):
    def wrapper(*args, **kwargs):
      data = request.get_json()
      try:
        validate(instance=data, schema=schema)
      except ValidationError as e:
        return Response(
          json.dumps({"error": e.message}), 
          mimetype="application/json", 
          status=400
        )
      return func(*args, **kwargs)
    return wrapper
  return decorator


def validate_product_id_param(func):
  # def decorator()
  def wrapper(self, *args, **kwargs):
    try:
      product_id=request.args
      validate(instance=product_id, schema=product_id_schema)
    except ValidationError as e:
      return Response(
        json.dumps({"error": e.message}), 
        mimetype="application/json", 
        status=400
      )
    return func(product_id, *args, **kwargs)
  return wrapper
  
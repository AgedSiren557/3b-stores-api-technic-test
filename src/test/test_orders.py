import pytest
from app import application
from bson import ObjectId


@pytest.fixture
def client():
  with application.test_client() as client:
    yield client
  
def test_orders_happy(client):
  data = { "order_id": str(ObjectId()), "products":[ { "sku": "ice-foo-coo-gal", "quantity": 5 } ]}
  response = client.post('/api/orders',json=data)
  assert response.status_code == 201
  assert response.json.get('message') == "Succesfull Operation"

def test_orders_existing_order_id(client):
  id = str(ObjectId())
  data = { "order_id": id, "products":[ { "sku": "ice-foo-coo-gal", "quantity": 5 } ]}
  client.post('/api/orders',json=data)
  response = client.post('/api/orders',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "UNIQUE constraint failed: orders.order_id"
  
def test_orders_inexistance_sku(client):
  data = { "order_id": str(ObjectId()), "products":[ { "sku": "eci-foo-coo-gal", "quantity": 5 } ]}
  response = client.post('/api/orders',json=data)
  assert response.status_code == 204
  
def test_orders_invalid_sku(client):
  data = { "order_id": str(ObjectId()), "products":[ { "sku": "a", "quantity": 5 } ]}
  response = client.post('/api/orders',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "'a' does not match '^[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}$'"

def test_orders_sku_inexistant_id(client):
  data = { "order_id": True, "products":[ { "sku": "ice-foo-coo-gal", "quantity": 5 } ]}
  response = client.post('/api/orders',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "True is not of type 'string'"

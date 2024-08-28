import pytest
from app import application


@pytest.fixture
def client():
  with application.test_client() as client:
    yield client
  
def test_inventories_happy_path(client):
  data = {"stock": 5}
  response = client.patch('/api/inventories/product/1',json=data)
  assert response.status_code == 200
  assert response.json.get('message') == "Succesfull Operation"

def test_inventories_invalid_stock(client):
  data = {"stock": "a"}
  response = client.patch('/api/inventories/product/1',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "'a' is not of type 'integer'"
  
def test_inventories_invalid_id(client):
  data = {"stock": 5}
  response = client.patch('/api/inventories/product/a',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "<id_product> param must be a valid id"
  
def test_inventories_not_stock(client):
  data = {}
  response = client.patch('/api/inventories/product/1',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "'stock' is a required property"

def test_inventories_sku_inexistant_id(client):
  data = {"stock": 5}
  response = client.patch('/api/inventories/product/1000',json=data)
  assert response.status_code == 204

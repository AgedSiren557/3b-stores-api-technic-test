import pytest
import random
import string
from app import application


@pytest.fixture
def client():
  with application.test_client() as client:
    yield client
  
def test_products_happy_path_without_price(client):
  data = {'sku': generate_sku(), 'name': 'Ice cream of cookies and cream'}
  response = client.post('/api/products',json=data)
  assert response.status_code == 201
  assert response.json.get('message') == "Succesfull Operation"

def test_products_happy_path_with_price(client):
  data = {'sku': generate_sku(), 'name': 'Ice cream of cookies and cream', "price":"14.99"}
  response = client.post('/api/products',json=data)
  assert response.status_code == 201
  assert response.json.get('message') == "Succesfull Operation"

def test_products_not_sku(client):
  data = {'name': 'Ice cream of cookies and cream'}
  response = client.post('/api/products',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "'sku' is a required property"
  
def test_products_not_name(client):
  data = {'sku': generate_sku()}
  response = client.post('/api/products',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "'name' is a required property"

def test_products_sku_without_format(client):
  data = {'sku': "ice-foo-gaa", 'name': 'Ice cream of cookies and cream'}
  response = client.post('/api/products',json=data)
  assert response.status_code == 400
  assert response.json.get('error') == "'ice-foo-gaa' does not match '^[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}$'"


def generate_sku():
  def generate_part(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

  sku = '-'.join(generate_part(3) for _ in range(4))
  return sku
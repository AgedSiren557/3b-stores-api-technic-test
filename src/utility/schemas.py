inventories_schema = {
  "type": "object",
  "properties": {
    "stock": {"type": "integer"},
  },
  "required": ["stock"],
  "additionalProperties": False
}

orders_schema = {
  "type": "object",
  "properties": {
    "order_id": {"type": "string"},
    "products":{
      "type": "array",
      "items":  {
        "type": "object",
        "properties": {
          "sku": {
            "type": "string",
            "pattern": "^[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}$"
          },
          "quantity": {"type": "number"}
        },
        # "required": ["sku", "quantity"]
      }
    }
  },
  "required": ["products", "order_id"],
  "additionalProperties": False
}
products_schema = {
  "type": "object",
  "properties": {
    "sku": {"type": "string","pattern": "^[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}-[a-zA-Z]{3,}$"},
    "name": {"type": "string",},
    "stock":{"type": "number",},
    "price":{"type": "string",}
  },
  "required": ["sku","name"],
  "additionalProperties": False
}

product_id_schema = {
  "type": "integer",
}
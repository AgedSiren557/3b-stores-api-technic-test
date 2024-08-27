import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.resources.urls import url_patterns
from dotenv import load_dotenv
from local_db import create_tables_db

load_dotenv()

application = Flask("3b_app")
CORS = CORS(application, resources={r"/cartec/*": {"origins": "*"}})
application.config['CORS_HEADERS'] = 'Content-Type'

api = Api(application)
url_patterns(api)

# if os.getenv("ENVIROMENT", "PRODUCTION") is "LOCAL":
create_tables_db()

if __name__ == "__main__":
  application.debug = True
  application.run()

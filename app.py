import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from utils.schema.models import db,ma
from utils.authentication.auth_helper import jwt


load_dotenv()

app = Flask(__name__)

#SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshit%402003@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

#JWT Configuration
app.config['JWT_PRIVATE_KEY'] = open('private.pem', 'r').read()
app.config['JWT_PUBLIC_KEY'] = open('public.pem', 'r').read()
app.config['JWT_ALGORITHM'] = 'RS256'
app.config['BLACKLIST_ENABLED'] = True
app.config['BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

#JWT Token Expiration
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

#Migrate Configuration
migrate = Migrate(app, db)

#Initialize Database
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)

@app.route('/')
def index():
    return jsonify({'message': 'The Project Management API is running'})


from utils.schema.models import models
app.register_blueprint(models)

from utils.authentication.auth_helper import auth_helper
app.register_blueprint(auth_helper)

from utils.apis.registration import company_registration
app.register_blueprint(company_registration, url_prefix='/v1')

from utils.apis.authenticate import authentication
app.register_blueprint(authentication, url_prefix='/v1')

from utils.apis.clients import clients
app.register_blueprint(clients, url_prefix='/v1')


if __name__ == "__main__":
    app.run(debug=True)
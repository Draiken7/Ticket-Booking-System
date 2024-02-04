from configs.config import devConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from flask_caching import Cache

from models import db, Users, Roles


app = Flask(__name__)
app.config.from_object(devConfig)

# Create a Datastore Object
datastore = SQLAlchemyUserDatastore(db, Users, Roles)


# Create a security Instance
security = Security(app, datastore)

# Create a cache instance with the current app
cache = Cache(app)
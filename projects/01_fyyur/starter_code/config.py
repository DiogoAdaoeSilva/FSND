import os
from app import app

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://diogocruz@localhost:5432/fyyurapp' 







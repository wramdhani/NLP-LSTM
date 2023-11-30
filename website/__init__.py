import os
from flask import Flask
from flask_session import Session

def create_app():
  app = Flask(
    __name__
  )

  # Set the secret key and configure the session to use filesystem storage
  app.config['SECRET_KEY'] = os.urandom(16)
  app.config['SESSION_TYPE'] = 'filesystem'

  Session(app)  # Initialize the session

  from .routes.views import views
  from .routes.auth import auth

  app.register_blueprint(views, url_prefix="/")
  app.register_blueprint(auth, url_prefix="/auth/")


  return app
from flask import Blueprint

authenticate = Blueprint('auth', __name__)

from app.auth import views


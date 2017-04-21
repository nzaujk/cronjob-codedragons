from flask import Blueprint

administrator = Blueprint('admin', __name__)

from . import views



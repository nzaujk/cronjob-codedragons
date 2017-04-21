from flask import Blueprint

store_blueprint = Blueprint('store', __name__, template_folder='templates')

from app.store import views

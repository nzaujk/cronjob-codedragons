from flask import flash, redirect, render_template, request, url_for, Blueprint, session  # current_app
from .forms import ProductForm
from app import db
from app.models import Store, Product, User
from flask_login import login_required, current_user

product_blueprint = Blueprint('product', __name__)


# Your stores page routing
@product_blueprint.route('/overview/<int:id>', methods=['GET', 'POST'])
def overview(id):
    store = Store.query.get(id)

    session['store_id'] = id

    display_product = Product.query.filter_by(store_home=store.id).all()
    all_products = len(display_product)

    return render_template('/product/overview.html', display_products=display_product, all_products=all_products)


# Add product route
@product_blueprint.route('/product/addproduct', methods=['GET', 'POST'])
@login_required
def product():
    "Creates a new product in a store"
    form = ProductForm()
    if request.method == "GET":
        return render_template('product/addproduct.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            store = session['store_id']
            created_products = Product(product_name=form.product_name.data, product_description=form.product_desc.data, store_home=store)

            db.session.add(created_products)
            db.session.commit()
            flash("Product added successfully!")
            return redirect(url_for('product.overview', id=store))

        return render_template('product/overview.html')

# -*- coding: utf-8 -*-

from flask import flash, redirect, render_template, request, url_for, Blueprint  # current_app
from app import db
from app.models import Store, User, Product
from flask_login import login_required, current_user
from .forms import StoreForm


# Config
store_blueprint = Blueprint(
    'store', __name__
)


# Routes

@store_blueprint.route('/overview', methods=['GET'])
@login_required
def overview():
    """
    Landing page when user logs in

    Displays current_user's availbable stores if any
    """
    user = User.query.filter_by(id=current_user.id).first()
    display_store = user.user_stores.all()
    all_stores = 0
    for i in display_store:
        all_stores += 1
    return render_template('/store/overview.html', display_stores=display_store, all_stores=all_stores)


@store_blueprint.route('/addstore', methods=['GET', 'POST'])
@login_required
def store():
    """
    Creates a new store
    """
    form = StoreForm()
    if request.method == "GET":
        return render_template('store/addstore.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            created_stores = Store(store_name=form.store_name.data, store_description=form.store_desc.data, store_owner=current_user.id)

            user.user_stores.append(created_stores)
            db.session.add(created_stores)
            db.session.commit()
            flash("Store added successfully!")
            return redirect(request.args.get('next') or url_for('store.overview'))

        user = User.query.filter_by(id=current_user.id).first()
        display_store = user.user_stores.all()
        display_store.store_owner
        all_stores = 0
        for i in display_store:
            all_stores += 1

        return render_template('store/addstore.html', display_stores=display_store, all_stores=all_stores)

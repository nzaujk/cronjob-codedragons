from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.auth import authenticate
from .forms import LoginForm, RegistrationForm
from app import db
from app.models import StoreOwner


@authenticate.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        store_owner = StoreOwner(email=form.email.data,username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, password=form.password.data)

        # add store owner to the database
        db.session.add(store_owner)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@authenticate.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        store_owner = StoreOwner.query.filter_by(email=form.email.data).first()
        if store_owner is not None and store_owner.verify_password(
                form.password.data):
            login_user(store_owner)
            return redirect(url_for('home.dashboard'))

        if store_owner.is_admin:
            return redirect(url_for('home.admin_dashboard'))
        else:
            return redirect(url_for('home.dashboard'))
            # when login details are incorrect

    else:
        flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@authenticate.route('/logout')
@login_required
def logout():

    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

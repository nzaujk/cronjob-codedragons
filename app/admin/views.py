from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from .forms import StoreTypeForm, StoreOwnerAssignForm, RoleForm
from app.models import StoreType, StoreOwner, Role
from app.admin import administrator
from .. import db


def check_admin():
    """
    Prevent non-admin from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@administrator.route('/stores', methods=['GET', 'POST'])
@login_required
def list_stores():

    check_admin()

    stores = StoreType.query.all()

    return render_template('admin/stores/stores.html', stores=stores, title="Stores")


@administrator.route('/stores/add', methods=['GET', 'POST'])
@login_required
def add_product():
    # add a store to the database
    check_admin()
    add_store = True
    form = StoreTypeForm()
    if form.validate_on_submit():
        store = StoreType(name=form.name.data, description=form.description.data)
        try:
            # add store to the database
            db.session.add(store)
            db.session.commit()
            flash('You have successfully added a new store.')
        except:

            flash('Error: The Store name already exists.')

        # redirect
        return redirect(url_for('admin.list_stores'))

    # load store template
    return render_template('admin/stores/stores.html', action="Add",
                           add_product=add_store, form=form,
                           title="Add Product")


@administrator.route('/stores/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_stores(store_id):

    check_admin()
    add_store = False

    stores = StoreType.query.get_or_404(id)
    form = StoreTypeForm(obj=stores)
    if form.validate_on_submit():
        stores.name = form.name.data
        stores.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the store.')

        return redirect(url_for('admin.list_stores'))

    form.description.data = stores.description
    form.name.data = stores.name
    return render_template('admin/stores/store.html', action="Edit",
                           add_store=add_store, form=form,
                           stores=stores, title="Edit stores")


@administrator.route('/stores/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_stores(store_id):

    check_admin()

    stores = StoreType.query.get_or_404(id)
    db.session.delete(stores)
    db.session.commit()
    flash('You have successfully deleted your store.')

    # redirect to the stores page
    return redirect(url_for('admin.list_stores'))

    return render_template(title="Delete Store")


@administrator.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@administrator.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    check_admin()
    add_role = True
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@administrator.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@administrator.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@login_required
def list_storeowners():

    check_admin()
    storeowners = StoreOwner.query.all()
    return render_template('admin/storeowners/storeowners.html',
                           storeowners=storeowners, title='Storeowners')


@administrator.route('/storeowners/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_storeowners(id):

    check_admin()

    storeowner = StoreOwner.query.get_or_404(id)

    if storeowner.is_admin:
        abort(403)

    form = StoreOwnerAssignForm(obj=storeowner)
    if form.validate_on_submit():
        storeowner.store = form.stores.data
        storeowner.role = form.role.data
        db.session.add(storeowner)
        db.session.commit()
        flash('You have successfully assigned a store and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_storeowners'))

    return render_template('admin/storeowners/storeowner.html',
                           storeowner=storeowner, form=form,
                           title='Approve Store Owner')
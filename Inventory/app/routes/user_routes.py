from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.forms.user_forms import UserForm, PasswordForm
from app.utils.decorators import admin_required

bp = Blueprint('user', __name__)

@bp.route('/users')
@login_required
@admin_required
def list_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.username).paginate(page=page, per_page=10)
    return render_template('users/list_users.html', users=users)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    password_form = PasswordForm()
    
    if form.validate_on_submit() and password_form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            department=form.department.data,
            is_active=form.is_active.data
        )
        user.set_password(password_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('user.list_users'))
    
    return render_template('users/add_user.html', title='Add User', 
                         form=form, password_form=password_form)

@bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('user.list_users'))
    
    return render_template('users/edit_user.html', title='Edit User', 
                         form=form, user=user)
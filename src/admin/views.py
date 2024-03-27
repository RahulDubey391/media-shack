from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from src import db
from werkzeug.security import generate_password_hash,check_password_hash
from src.models import User, BlogPost
from src.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from src.admin.forms import AddContentForm
from src.admin.decorator import admin_required

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
@admin_required  # Apply the admin access decorator
def dashboard():
    # Render the admin dashboard template
    return render_template('admin/dashboard.html')

@admin.route('/add_content', methods=['GET', 'POST'])
@login_required
@admin_required  # Apply the admin access decorator
def add_content():
    form = AddContentForm()
    if form.validate_on_submit():
        # Create a new BlogPost instance and add it to the database
        new_post = BlogPost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Content added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_content.html', form=form)
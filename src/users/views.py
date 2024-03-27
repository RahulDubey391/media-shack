from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from src import db
from werkzeug.security import generate_password_hash,check_password_hash
from src.models import User, MediaPost
from src.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('users.register'))

        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            is_admin=form.is_admin.data
        )

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)

            if form.is_admin.data and user.is_admin:
                # If logging in as admin and user is admin, redirect to admin dashboard
                return redirect(url_for('admin.dashboard'))
            else:
                # If logging in as regular user or user is not admin, redirect to regular user dashboard
                return redirect(url_for('core.index'))

        flash('Invalid email or password.', 'error')

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))



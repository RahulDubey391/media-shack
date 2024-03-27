from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET'])
def login():
    return render_template('admin/login.html')

@admin.route('/logout', method=['GET'])
def logout():
    return render_template('admin/logout.html')

@admin.route('/addMedia', methods=['GET','POST'])
def addMedia():
    return render_template('add_media.html')
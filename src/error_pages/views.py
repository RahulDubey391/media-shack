from flask import Flask, Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def get_404(error):
    return render_template('error_pages/404.html')

@error_pages.app_errorhandler(403)
def get_403(error):
    return render_template('error_pages/403.html')
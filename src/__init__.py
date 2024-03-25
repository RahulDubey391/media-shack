from flask import Flask

app = Flask(__name__)

from src.error_pages.views import error_pages
app.register_blueprint(error_pages)

from src.core.views import core
app.register_blueprint(core)
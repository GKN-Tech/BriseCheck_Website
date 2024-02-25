from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'brisecheck@ismyfunproject'

    from .views import views
    from .pages import pages

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(pages, url_prefix='/')

    return app



import json

from flask_mail import Mail
from flask import Flask, request, session

from app.env import db
from config import config

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.config.from_pyfile('config/config.py')

db.init_app(app)
app.config['DB'] = db

mail = Mail()
mail.init_app(app)
app.config['MAIL'] = mail

app.secret_key = config.SECRET_KEY

with app.app_context():

    @app.after_request
    def after_login_method(response):

        if not request.cookies.get('token'):
            session["current_user"] = None

        if request.endpoint == 'auth.login' and response.status_code == 200:
            current_user = json.loads(response.get_data().decode('utf-8'))
            session["current_user"] = current_user["user"]

        return response
    
    from app.post_actions import function_dict
    app.config['after_USERSHUB_request'] = function_dict

    from app import routes
    app.register_blueprint(routes.bp, url_prefix='/')
    
    from pypnusershub import routes_register
    app.register_blueprint(routes_register.bp, url_prefix='/pypn/register')
    from pypnusershub import routes
    app.register_blueprint(routes.routes, url_prefix='/pypn/auth')




if __name__ == '__main__':
    app.run(debug=True, port=1234)
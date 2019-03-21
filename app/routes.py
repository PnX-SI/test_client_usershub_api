from flask import (
    Blueprint, render_template, request, session, url_for, redirect, current_app
)

from pypnusershub.db.models import User, AppUser

MAIL = current_app.config.get('MAIL', None)

bp = Blueprint('test_api_usershub', __name__)


def get_user(id_role):
    user = User.query.get(id_role)
    return user


def get_users(id_application):
    users = AppUser.query.filter(
        AppUser.id_application == id_application
    ).all()
    return users


@bp.route('/login')
def login():
    '''
        page de connection
    '''
    return render_template(
        'login.html',
        id_app=current_app.config.get('ID_APP', None),
        url_application=current_app.config.get('URL_APPLICATION', None),
    )


@bp.route('/')
@bp.route('/users')
def users_list():
    '''
        Liste des utilisateurs actuels pour l'applcation
    '''
    id_app = current_app.config.get('ID_APP', None)
    users = get_users(id_app)
    return render_template(
        'users.html',
        users=users
    )


@bp.route('/user_form')
@bp.route('/user_form/<int:id_role>')
def user_form(id_role=None):
    user = {}
    if id_role:
        user = get_user(id_role).as_dict()

    return render_template(
        'user_form.html',
        user=user,
        liste_organismes=[{"id_organism": 1, "nom_organism": "test"}]
    )


@bp.route('/create_user')
def create_user():

    token = request.args.get('token', "")

    return render_template(
        'create_user.html',
        token=token,
        id_application=current_app.config.get('ID_APP', None)
    )


@bp.route('/change_password', methods=['GET'])
@bp.route('/change_password/<string:token>', methods=['GET'])
def change_password(token=None):
    '''
        page pour recreer un mot de passe
    '''

    return render_template('change_password.html', token=token)

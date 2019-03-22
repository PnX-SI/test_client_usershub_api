from flask import (
    Blueprint, render_template, request, session, url_for, redirect, current_app
)

from pypnusershub.db.models import User, AppUser, ProfilsForApp

MAIL = current_app.config.get('MAIL', None)
DB = current_app.config.get('DB', None)

bp = Blueprint('test_api_usershub', __name__)


def get_user(id_role):
    user = User.query.get(id_role)
    return user

def get_user_app(id_role, id_application):
    try:
        user = AppUser.query.filter(
            AppUser.id_application == id_application
        ).filter(
            AppUser.id_role == id_role
        ).one()
    except:
        user = None

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

@bp.route('/change_privilege/<string:id_role>', methods=['GET'])
def change_privilege(id_role):
    '''
        page pour changer le niveau de droit d'un utilisateur
    '''
    id_application = current_app.config.get('ID_APP', None)
    user = get_user_app(id_role, id_application)
    if not user:
        user = get_user(id_role)
    print(user.as_dict())
    privileges = ProfilsForApp.query.filter(
        ProfilsForApp.id_application==id_application
    ).all()

    profils = [
        {"id_profil": p.profil.id_profil, "code_profil": p.profil.code_profil, "nom_profil":p.profil.nom_profil}
        for p in privileges
    ]
    return render_template(
        'change_privilege.html',
        user=user.as_dict(),
        profils=profils,
        id_application=id_application
    )

@bp.route('/add_user_to_app', methods=['GET'])
def add_user_to_app():

    id_application = current_app.config.get('ID_APP', None)
    return render_template(
        'add_user_to_app.html',
        id_application=id_application
    )
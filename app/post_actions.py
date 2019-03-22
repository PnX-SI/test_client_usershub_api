from flask import (
    Blueprint, render_template, current_app, url_for
)
from flask_mail import Message
from pypnusershub.db.models import Application, User
from pypnusershub.db.models_register import TempUser


config = current_app.config
MAIL = config.get('MAIL', None)
DB = config.get('DB', None)

bp = Blueprint('oeasc_api_mail', __name__)


def send_mail(recipients, subject, msg_html):

    if not MAIL and config.get('ANIMATEUR_APPLICATION_MAIL', None):

        return {"msg": "les paramètres d'envoi de mail ne sont pas correctement définis"}

    application = DB.session.query(Application).filter(
        Application.id_application == config['ID_APP']
    ).one()

    with MAIL.connect() as conn:

        msg = Message(
            '[' + application.nom_application + '] ' + subject,
            sender=config['ANIMATEUR_APPLICATION_MAIL'],
            recipients=recipients)

        msg.html = msg_html

        conn.send(msg)

    return {'msg': 'ok'}


def create_temp_user(data):

    token = data.get('token', None)

    role = DB.session.query(TempUser).filter(TempUser.token_role == token).first()

    if not role:

        return {"msg": token + " : ce token n'est pas associé à un compte temporaire"}

    url_validation = config['URL_APPLICATION'] + url_for('test_api_usershub.create_user', token=token)

    recipients = [role.email]
    subject = 'demande de création de compte'
    msg_html = render_template(
        'mail/create_temp_user.html',
        url_validation=url_validation,
        identifiant=role.identifiant,
        config=config
    )

    return send_mail(
        recipients,
        subject,
        msg_html
    )


def valid_temp_user(data):

    role = data

    if not role:
        return {"msg": "Pas de role pour valid_temp_user"}

    recipients = [config['ANIMATEUR_APPLICATION_MAIL'], config['ADMIN_APPLICATION_MAIL']]
    subject = ' [ANIMATEUR] création d'' un nouvel utilisateur'

    msg_html = "<p>Un nouvel utilisateur vient de s'enregister</p>"
    msg_html += "<hr><p>Identifiant : {}</p><p>E-mail : {}</p><p>Nom : {}</p><p>Prenom : {}</p>".format(
        role['identifiant'].strip(),
        role['email'].strip(),
        role['nom_role'].strip(),
        role['prenom_role'].strip()
    )

    return send_mail(
        recipients,
        subject,
        msg_html
    )


def update_user(data):

    role = data

    if not role:
        return {"msg": "Pas de role pour valid_temp_user"}

    recipients = [
        config['ANIMATEUR_APPLICATION_MAIL'], config['ADMIN_APPLICATION_MAIL']
    ]
    subject = '[ANIMATEUR] Modification d'' un utilisateur'
    print(role)
    msg_html = "<p>Un utilisateur à modifier ses informations</p>"
    msg_html += "<hr><p>Identifiant : {}</p><p>E-mail : {}</p><p>Nom : {}</p><p>Prenom : {}</p>".format(
        role['identifiant'].strip(),
        role['email'].strip(),
        role['nom_role'].strip(),
        role['prenom_role'].strip()
    )

    return send_mail(
        recipients,
        subject,
        msg_html
    )


def change_application_right(data):

    role = data['role']

    id_droit = data['id_droit']

    if not role:

        return {"msg": "Pas de role pour valid_temp_user"}

    recipients = [role['email']]
    subject = ' modification de votre niveau de droit '

    msg_html = render_template(
        'mail/change_application_privilege.html',
        role=role,
        id_droit=id_droit
    )

    return send_mail(
        recipients,
        subject,
        msg_html
    )


def create_cor_role_token(data):

    token = data['token']
    id_role = data['id_role']

    role = DB.session.query(User).filter(id_role == User.id_role).first()

    url_validation = config['URL_APPLICATION'] + url_for(
        'test_api_usershub.change_password', token=token
    )

    recipients = [role.email]
    subject = 'changement de mot de passe'
    msg_html = render_template(
        'mail/change_password.html',
        url_validation=url_validation
    )

    return send_mail(
        recipients,
        subject,
        msg_html
    )

def add_application_right_to_role(data):
    role = data

    if not role:

        return {"msg": "Pas de role pour valid_temp_user"}

    recipients = [role['email']]
    subject = " Inscription à l'aplication "

    url_login = config['URL_APPLICATION'] + url_for(
        'test_api_usershub.login'
    )

    msg_html = render_template(
        'mail/add_user_to_app.html',
        role=role,
        url_login=url_login
    )

    return send_mail(
        recipients,
        subject,
        msg_html
    )


function_dict = {
    'create_cor_role_token': create_cor_role_token,
    'create_temp_user': create_temp_user,
    'valid_temp_user': valid_temp_user,
    'change_application_right': change_application_right,
    'update_user': update_user,
    'add_application_right_to_role': add_application_right_to_role
}

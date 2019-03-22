# test_client_usershub_api
Application permettant de tester les fonctionnalités de l'api de usershub

Cette application est uniquement destinée à réaliser des tests

## Prerequis
Avoir une version de Userhub qui fonctionne.
Pour le moment la version fonctionnelle est la branche develop de https://github.com/amandine-sahl/UsersHub


## Installation et configuration

```
 ./install_app.sh
```

Ouvrir et modifier le fichier `config.py`

Pour le moment l'application ne fonctionne qu'avec la version develop du module pypnusershub du dépot https://github.com/amandine-sahl/UsersHub-authentification-module

## Lancer l'application

```
 source venv/bin/activate
 python server.py
```
Aller sur la navigateur à l'adresse localhost:1234


## Fonctionnalités

* Login
* Changement de mot de passe
* Ajouter un utilisateur
* Mette à jour un utilisateur
* Changer le niveau de droit d'un utilisateur [TODO]

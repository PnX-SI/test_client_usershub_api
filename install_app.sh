#!/bin/bash

. config/settings.ini

echo "Création du fichier de configuration ..."
if [ ! -f config.py ]; then
  cp config/config.py.sample config/config.py

  echo "préparation du fichier config.py..."
  sed -i "s/SQLALCHEMY_DATABASE_URI = .*$/SQLALCHEMY_DATABASE_URI = \"postgresql:\/\/$user_pg:$user_pg_pass@$db_host:$db_port\/$db_name\"/" config/config.py


fi
#installation des librairies
cd app/static/
npm install
cd ../..

#Installation du virtual env
echo "Installation du virtual env..."


if [[ $python_path ]]; then
  virtualenv -p $python_path $venv_dir
else
  virtualenv $venv_dir
fi

source $venv_dir/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

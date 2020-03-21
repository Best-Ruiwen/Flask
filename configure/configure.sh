#!/bin/bash


#Nginx config
path=$(pwd)
`sed -i "s!root!$path!g" default`
sudo apt -y install nginx
`sudo rm /etc/nginx/sites-available/default`
`sudo mv default /etc/nginx/sites-available/`


#Python config
pip3 install flask pycryptodome redis


#Uwsgi config
sudo apt-get install libpython3.5-dev
pip3 install uwsgi

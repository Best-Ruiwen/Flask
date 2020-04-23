#!/bin/bash


#Nginx configuration
path=$(pwd)
`sed -i "s!root!$path!g" default`
sudo apt -y install nginx
`sudo rm /etc/nginx/sites-available/default`
`sudo mv default /etc/nginx/sites-available/`


#Redis server configuration


#Python configuration
pip3 install flask pycryptodome redis


#Uwsgi configuration
sudo apt-get install libpython3.5-dev
pip3 install uwsgi

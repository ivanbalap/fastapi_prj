#!/usr/bin/env bash

# apt update
# apt upgrade -y

# apt install zsh
# sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

sudo apt-get install -y -q build-essential git unzip zip nload tree
sudo apt-get install -y -q python3-pip python3-dev python3-venv

sudo apt install fail2ban -y

# ufw allow 22
ufw allow 2435
ufw aloow 80
ufw allow 443
ufw enable

apt install acl -y
useradd -M apiuser
usermod -L apiuser
# setfacl -m u:apiuser:rwx /apps/logs/weather_api

mkdir /apps
chmod 777 /apps
mkdir /apps/logs
mkdir /apps/logs/weather_api
mkdir /apps/logs/weather_api/app_log
# chmod 777 /apps/logs/weather_api
cd /apps
setfacl -m u:apiuser:rwx /apps/logs/weather_api

cd /apps
python3 -m venv venv
source /apps/venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade httpie glances
pip install --upgrade gunicorn uvloop httptools

cd /apps
git clone https://github.com/ivanbalap/fastapi_prj app_repo

cd /apps/app_repo/ch08-deployment
pip install -r requirements.txt

cp /apps/app_repo/ch08-deployment/server/units/weather.service /ect/systemd/system

systemctl start weather
systemctl status weather
systemctl enable weather

apt install nginx

rm /ect/nginx/sites-enabled/default

cp /apps/app_repo/ch08-deployment/server/nginx/weather.nginx /etc/nginx/sites-enabled/
update-rc.d nginx enable
service nginx restart

add-apt-repository ppa:certbot/certbot
apt install python-certbot-nginx
certbot --nginx -d weatherapi.talkpython.com
#!/bin/sh
VE_DIR=./.ve
# hack -- check if running in docker
if [ ! -e "test.sh" ]; then cd /opt/app ; fi
# install extra
if [ -e "/etc/lsb-release" ]; then
    DEBCONF_FRONTEND=noninteractive apt-get install -y python-setuptools python-dev
fi
easy_install virtualenv
virtualenv --no-site-packages $VE_DIR
$VE_DIR/bin/pip install -r requirements.txt
$VE_DIR/bin/python manage.py test web

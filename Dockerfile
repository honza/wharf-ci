FROM base
MAINTAINER Wharf-CI "https://github.com/honza/wharf-ci"
RUN apt-get -qq update
RUN apt-get install -y python-dev python-setuptools libxml2-dev libxslt-dev libmysqlclient-dev git-core supervisor
RUN easy_install pip
RUN pip install uwsgi
ADD . /opt/app
RUN find /opt/app -name "*.db" -delete
ADD .docker/supervisor.conf /opt/supervisor.conf
RUN pip install -r /opt/app/requirements.txt
RUN (cd /opt/app && python manage.py syncdb --noinput)
RUN (cd /opt/app && python manage.py migrate)
EXPOSE 8000
CMD ["supervisord", "-c", "/opt/supervisor.conf", "-n"]

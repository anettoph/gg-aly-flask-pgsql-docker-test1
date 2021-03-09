FROM tiangolo/uwsgi-nginx-flask:latest

# ENV LISTEN_PORT 8787
ENV UWSGI_INI /app/uwsgi.ini

RUN pip install -r /app/requirements.txt
RUN sudo apt update -y && sudo apt upgrade -y; \
    python -m pip install --upgrade pip; \
    pip install -r /app/requirements.txt; \
    cd /app; \
    flask shell; \
    from app.models import User \
    from app import db \
    u = User(username='admin', email='admin@mail.no') \
    u.set_password('admin') \
    db.session.add(u) \
    db.session.commit() \
    exit()
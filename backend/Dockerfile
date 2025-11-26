FROM python:alpine
WORKDIR /app
RUN pip install django psycopg2-binary django-prometheus && \
    apk add --no-cache netcat-openbsd curl
#RUN django-admin startproject blog .
COPY . /app/
#RUN python manage.py startapp twi
#RUN python manage.py makemigrations
#RUN python manage.py sqlmigrate twi
#RUN python manage.py migrate
#RUN python manage.py createsuperuser
EXPOSE 8000
CMD echo 'App starting' && nc -z localhost 5432 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

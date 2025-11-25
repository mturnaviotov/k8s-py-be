FROM python:alpine
WORKDIR /app
RUN pip install django
RUN django-admin startproject blog .
COPY . /app/
#RUN python manage.py startapp twi
#RUN python manage.py makemigrations
#RUN python manage.py sqlmigrate twi
RUN python manage.py migrate
RUN python manage.py createsuperuser
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000

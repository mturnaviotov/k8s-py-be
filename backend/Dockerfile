FROM python:alpine
ENV PORT=8000

WORKDIR /app
COPY . /app/
RUN pip install django psycopg2-binary django-prometheus && \
    apk add --no-cache netcat-openbsd curl && \
    chmod +x /app/start.sh
#RUN django-admin startproject blog .
#RUN python manage.py startapp twi
#RUN python manage.py makemigrations
#RUN python manage.py sqlmigrate twi
#RUN python manage.py migrate
#RUN python manage.py createsuperuser
EXPOSE ${PORT}
CMD ["sh", "/app/start.sh"]

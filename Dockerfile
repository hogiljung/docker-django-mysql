FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin"

WORKDIR /app/src
CMD python manage.py migrate; python manage.py runserver 0.0.0.0:8000
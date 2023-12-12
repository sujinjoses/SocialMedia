FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt update -y

RUN apt install -y python3-dev build-essential


RUN mkdir /code

WORKDIR /code

RUN pip3 install pipenv

COPY Pipfile /code/

RUN pipenv install --dev


COPY . /code/

WORKDIR /code/social_media


CMD [ "pipenv", "run", "gunicorn", "social_media.wsgi", "-b", "0.0.0.0:8000", "--access-logfile" ,"-", "--error-logfile", "-" ]

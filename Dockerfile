FROM python:3.10

RUN useradd --create-home userapi
WORKDIR  /flask_project

RUN pip install -U pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
COPY ./ .
RUN chown -R userapi:userapi ./
USER userapi

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
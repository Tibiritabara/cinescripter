FROM python:3.11-slim-buster

WORKDIR /app

RUN python -m pip install pipenv

COPY ./Pipfile ./Pipfile.lock ./

RUN pipenv install --system --deploy

COPY ./src ./

ENV PYTHONPATH=$PYTHONPATH:/app

CMD ["python", "-m", "main.py", "-h"]

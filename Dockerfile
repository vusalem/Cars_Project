FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./turbo_az .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
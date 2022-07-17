FROM python:3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=$PATH:/app
ENV PYTHONPATH /app

RUN apt-get update && \
    apt-get -y install \
    default-libmysqlclient-dev \
    python3-dev \
    netcat

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

# ------------------- 1 Dockerfile -------------------

## указываем образ на основе
## которого будет создан контейнер
#FROM python:3.8
#
## Создаем рабочую директорию внутри контейнера
#WORKDIR /usr/src/car_park
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV PATH=$PATH:/usr/src/car_park
#ENV PYTHONPATH /usr/src/car_park
#
#
## копируем файл req.txt
#COPY ./req.txt /usr/src/req.txt
#
## выполняем установу зависимостей
#RUN pip install --upgrade pip && pip install -r /usr/src/req.txt
#
## копируем проект в ворк_дир контейнера
#COPY . /usr/src/car_park


# ------------------------------------------------------------





#EXPOSE 8000

# выполняем команду python manage.py runserver 0.0.0.0:8000
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#WORKDIR /web_django
#
#COPY requirements.txt /web_django/
#
#RUN pip install --upgrade pip && pip install -r requirements.txt
#
#ADD . /web_django/
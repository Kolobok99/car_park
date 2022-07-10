# указываем образ на основе
# которого будет создан контейнер
FROM python:3.8


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Создаем рабочую директорию внутри контейнера
WORKDIR /usr/src/car_park

# копируем файл req.txt
COPY ./req.txt /usr/src/req.txt

# выполняем установу зависимостей
RUN pip install --upgrade pip && pip install -r /usr/src/req.txt

# копируем проект в ворк_дир контейнера
COPY . /usr/src/car_park

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
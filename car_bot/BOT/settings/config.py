# Загушка для использования ORM
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
django.setup()

# токен выдается при регистрации приложения
TOKEN = '5585708488:AAEbuD6Hv5lGhxlDhNstDSXl6ylmfYCIkXE'

COUNT = 0

# названия команд
COMMANDS = {
    'START': "start",
}
import datetime

from cabinet.models import Car, Application
from car_park.celery import app


@app.task
def check_last_inspection():
    cars = Car.objects.all()

    today = datetime.date.today()
    # today = pytz.utc.localize(today)

    # Сравнимаем текущую дату с датой последнего осмотра каждого авто
    for car in cars:
        time_delta = today - (car.last_inspection + datetime.timedelta(days=365))
        if time_delta <= datetime.timedelta(days=30):
            new_app = Application()
            new_app.type_id = 1
            new_app.owner_id = 1
            new_app.car = car
            new_app.description = "АВТОМАТИЧЕСКИ!!!"
            new_app.save()
            print(f"Заявка №{new_app.pk} создана!")
        else:
            print("Нет подходящий машин!")
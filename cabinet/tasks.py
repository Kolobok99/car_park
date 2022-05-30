import datetime

from django.core.mail import send_mail

from cabinet.models import Car, Application, FuelCard
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
            try:
                go = car.applications.get(owner=None)
            except:
                go = None
            if go:
                print("Заявка уже создана!")
            else:
                new_app = Application()
                new_app.type_id = 1
                new_app.car = car
                new_app.description = "АВТОМАТИЧЕСКИ!!!"
                new_app.save()
                print(f"Заявка №{new_app.pk} создана!")

        else:
            print("Нет подходящий машин!")

@app.task
def send_activation_code(driver_email, activation_code):
    """Отправляет код активации аккаунта"""
    send_mail(
        'Подтверждение регистрации',
        f'ВАШ КОД: {activation_code}',
        'izolotavin99@gmail.com',
        [driver_email],
        fail_silently=False
    )

@app.task
def a_plus_b(a, b):
    return a + b

@app.task
def delete_empty_card():
    cards = FuelCard.objects.filter(balance=0)
    for card in cards:
        card_pk = card.pk
        card.delete()
        print(f"{card_pk} удалена!")

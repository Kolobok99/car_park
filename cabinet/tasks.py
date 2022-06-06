import datetime

from django.core.mail import send_mail

from cabinet.models import Car, Application, FuelCard, MyUser, AutoDoc, UserDoc
from car_bot.models import Notifications
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
def check_car_docs_date():
    car_docs = AutoDoc.objects.all()
    today = datetime.date.today()

    for car_doc in car_docs:
        time_delta = today - car_doc.end_date
        if time_delta < 10:
            Notifications.objects.create(
                recipient=car_doc.owner.owner,
                content=f"Срок действия документа на машину {car_doc.owner.registration_number}"
                        f" истекает через {time_delta}",
                content_object=car_doc
            )

@app.task
def check_user_docs_date():
    user_docs = UserDoc.objects.all()
    today = datetime.date.today()

    for user_doc in user_docs:
        time_delta = today - user_doc.end_date
        if time_delta < 10:
            Notifications.objects.create(
                recipient=user_doc.owner,
                content=f"Срок действия {user_doc.type} документа истекает через {time_delta}",
                content_object=user_doc
            )


@app.task
def send_activation_code(driver_email, activation_code):
    """Отправляет код активации аккаунта"""
    send_mail(
        'Подтверждение регистрации',
        f'ВАШ КОД: {activation_code}',
        'zolotavin011@mail.ru',
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

@app.task
def create_note_about_ending_cards():
    cards = FuelCard.objects.filter(owner__isnull=True)
    if len(cards) < 2:
        Notifications.objects.create(
            recipient=MyUser.objects.get(role='m'),
            content=f"Заканчиваются карты, осталось {len(cards)} штуки",
            content_object=MyUser.objects.get(role='m')
        )

@app.task
def checking_timing_app():
    """Проверка просроченности заявки"""

    # Получить все заявки находящиеся в ремонте
    active_apps = Application.objects.filter(is_active=True)
    today = datetime.date.today()
    for app in active_apps:
        # Если заявка просрочена
        if app.end_date > today:
            # Уведомление механику
            Notifications.objects.create(
                recipient=app.engineer,
                content=f"Вы просрочили выполнение заявки {app.pk}",
                content_object=app
            )
            # Уведомление менеджеру
            Notifications.objects.create(
                recipient=MyUser.objects.get(role='m'),
                content=f"Механик ({app.engineer}) просрочил выполнение заявки {app.pk}",
                content_object=app
            )

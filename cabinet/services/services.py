import random
from itertools import chain
import random
import string
from django.utils.html import format_html

from cabinet import models
from car_bot.models import Notifications


class Context():
    """
       Примесь: Формирование контекста
    """

    def get_car_brands(self):
        """Возвращает все марки машин"""
        return models.CarBrand.objects.all()

    def get_drivers(self):
        """Возвращает всех водителей"""
        return models.MyUser.objects.filter(role='d')

    def get_regions(self):
        """Возвращает все коды регионов авто"""
        return models.Car.objects.all().values('region_code').distinct()

    def get_types_of_app(self):
        """Возвращает все типы заявок"""
        return models.TypeOfAppl.objects.all()

    def get_car_types_of_docs(self):
        """Возвращает все типы документов (авто) """
        return models.DocType.objects.filter(type='a')

    def get_man_types_of_docs(self):
        """Возвращает все типы документов (водители) """
        return models.DocType.objects.filter(type='m')

    def get_all_docs(self):
        """Возвращает документы (авто+водители)"""
        auto_doc = models.AutoDoc.objects.all()
        driver_doc = models.UserDoc.objects.all()
        query_set = list(chain(auto_doc, driver_doc))

        sorting_list_of_querysets = sort_by_date_start(query_set)
        return sorting_list_of_querysets

    def get_all_cards(self):
        """Возвращает все топливные карты"""
        return models.FuelCard.objects.all()

    def get_all_urgecny_types(self):
        """Возвращает все типы срочности заявок"""
        return models.Application.URGENCY_CHOISES

    def get_all_status_types(self):
        """Возвращает все типы статусов заявок"""
        return models.Application.STATUS_CHOISES

    def get_all_history(self):
        """Возвращает всю историю действий на сайте (почти для всех моделей)"""

        def changed_fields(obj):
            fields = []
            for f in obj:
                if f.prev_record:
                    delta = f.diff_against(f.prev_record)
                else:
                    delta = '-'
                fields.append(delta)
            return fields

        car_history = models.Car.history.all()
        app_history = models.Application.history.all()
        driver_history = models.MyUser.history.all()
        user_doc_history = models.UserDoc.history.all()
        car_doc_history = models.AutoDoc.history.all()

        query = list(chain(car_history,
                           app_history,
                           driver_history,
                           user_doc_history,
                           car_doc_history,
                           ))

        car_changed = changed_fields(car_history)
        app_changed = changed_fields(app_history)
        driver_changed = changed_fields(driver_history)
        user_doc_changed = changed_fields(user_doc_history)
        car_doc_changed = changed_fields(car_doc_history)


        changed_list = list(chain(car_changed,
                                  app_changed,
                                  driver_changed,
                                  user_doc_changed,
                                  car_doc_changed
                                  ))
        lists_with_history_and_changed_data = []


        for id, obj in enumerate(query):
            lll = []
            lll.append(obj)
            lll.append(changed_list[id])
            lists_with_history_and_changed_data.append(lll)

        l00 = lists_with_history_and_changed_data[0][0]
        hdate = l00.history_type
        print(f"{hdate=}")

        lists_with_history_and_changed_data = sort_by_history_date(lists_with_history_and_changed_data)

        for sub_list in lists_with_history_and_changed_data:
            model_name = str(sub_list[0].__class__)[33:-2]
            if sub_list[1] != '-':
                for change in sub_list[1].changes:
                    if model_name == 'Car':
                        change.field = models.Car._meta.get_field(change.field).verbose_name
                    elif model_name == 'Application':
                        change.field = models.Application._meta.get_field(change.field).verbose_name
                    elif model_name == 'MyUser':
                        change.field = models.MyUser._meta.get_field(change.field).verbose_name
                    elif model_name == 'UserDoc':
                        change.field = models.UserDoc._meta.get_field(change.field).verbose_name
                    elif model_name == 'AutoDoc':
                        change.field = models.AutoDoc._meta.get_field(change.field).verbose_name

        return lists_with_history_and_changed_data

def sort_by_history_date(list_to_sort):
    if len(list_to_sort) <= 1:
        return list_to_sort
    else:
        q = random.choice(list_to_sort)
        s_nums = []  # [меньше q]
        m_nums = []  # [больше q]
        e_nums = []  # [q]
        for elem in list_to_sort:
            # print(elem.start_date)
            if elem[0].history_date < q[0].history_date:
                # print("Меньше!")
                s_nums.append(elem)
            elif elem[0].history_date > q[0].history_date:
                m_nums.append(elem)
                # print("БОЛЬШЕ!")
            else:
                e_nums.append(elem)
        return sort_by_history_date(m_nums) + e_nums + sort_by_history_date(s_nums)


def sort_by_date_start(list_to_sort):
    if len(list_to_sort) <= 1:
        return list_to_sort
    else:
        q = random.choice(list_to_sort)
        s_nums = []  # [меньше q]
        m_nums = []  # [больше q]
        e_nums = []  # [q]
        for elem in list_to_sort:
            # print(elem.start_date)
            if elem.start_date < q.start_date:
                # print("Меньше!")
                s_nums.append(elem)
            elif elem.start_date > q.start_date:
                m_nums.append(elem)
                # print("БОЛЬШЕ!")
            else:
                e_nums.append(elem)
        return sort_by_date_start(s_nums) + e_nums + sort_by_date_start(m_nums)


def generator_activation_code():
    """Возвращает рандомную строку из 6 символов"""
    letters = string.ascii_lowercase
    length = 6
    rand_string = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", rand_string)
    return rand_string

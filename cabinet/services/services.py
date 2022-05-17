import random
from itertools import chain

from django.utils.html import format_html

from cabinet.models import CarBrand, MyUser, Car, TypeOfAppl, DocType, AutoDoc, UserDoc, FuelCard, Application


class Context():
    """
       Примесь: Формирование контекста
    """

    def get_car_brands(self):
        """Возвращает все марки машин"""
        return CarBrand.objects.all()

    def get_drivers(self):
        """Возвращает всех водителей"""
        return MyUser.objects.filter(role='d')

    def get_regions(self):
        """Возвращает все коды регионов авто"""
        return Car.objects.all().values('region_code').distinct()

    def get_types_of_app(self):
        """Возвращает все типы заявок"""
        return TypeOfAppl.objects.all()

    def get_car_types_of_docs(self):
        """Возвращает все типы документов (авто) """
        return DocType.objects.filter(type='a')

    def get_man_types_of_docs(self):
        """Возвращает все типы документов (водители) """
        return DocType.objects.filter(type='m')

    def get_all_docs(self):
        """Возвращает документы (авто+водители)"""
        auto_doc = AutoDoc.objects.all()
        driver_doc = UserDoc.objects.all()
        query_set = list(chain(auto_doc, driver_doc))

        sorting_list_of_querysets = sort_by_date_start(query_set)
        return sorting_list_of_querysets

    def get_all_cards(self):
        """Возвращает все топливные карты"""
        return FuelCard.objects.all()

    def get_all_urgecny_types(self):
        """Возвращает все типы срочности заявок"""
        return Application.URGENCY_CHOISES

    def get_all_status_types(self):
        """Возвращает все типы статусов заявок"""
        return Application.STATUS_CHOISES

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

        car_history = Car.history.all()
        app_history = Application.history.all()
        driver_history = MyUser.history.all()
        user_doc_history = UserDoc.history.all()
        car_doc_history = AutoDoc.history.all()

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
                        change.field = Car._meta.get_field(change.field).verbose_name
                    elif model_name == 'Application':
                        change.field = Application._meta.get_field(change.field).verbose_name
                    elif model_name == 'MyUser':
                        change.field = MyUser._meta.get_field(change.field).verbose_name
                    elif model_name == 'UserDoc':
                        change.field = UserDoc._meta.get_field(change.field).verbose_name
                    elif model_name == 'AutoDoc':
                        change.field = AutoDoc._meta.get_field(change.field).verbose_name

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

import random
from itertools import chain

from cabinet.models import CarBrand, MyUser, Car, TypeOfAppl, DocType, AutoDoc, UserDoc, FuelCard, Application


class Context():
    '''Получение контекста'''

    def get_car_brands(self):
        return CarBrand.objects.all()

    def get_drivers(self):
        return MyUser.objects.filter(role='d')

    def get_regions(self):
        return Car.objects.all().values('region_code').distinct()

    def get_types_of_app(self):
        return TypeOfAppl.objects.all()

    def get_car_types_of_docs(self):

        return DocType.objects.filter(type='a')

    def get_man_types_of_docs(self):
        return DocType.objects.filter(type='m')

    def get_all_docs(self):
        auto_doc = AutoDoc.objects.all()
        driver_doc = UserDoc.objects.all()
        query_set = list(chain(auto_doc, driver_doc))

        sorting_list_of_querysets = sort_by_date_start(query_set)
        return sorting_list_of_querysets

    def get_all_cards(self):
        return FuelCard.objects.all()

    def get_all_urgecny_types(self):
        return Application.URGENCY_CHOISES

    def get_all_status_types(self):
        return Application.STATUS_CHOISES


def sort_by_date_start(list_to_sort):
    if len(list_to_sort) <= 1:
        return list_to_sort
    else:
        q = random.choice(list_to_sort)
        s_nums = []  # [меньше q]
        m_nums = []  # [больше q]
        e_nums = []  # [q]
        for elem in list_to_sort:
            # print(elem.date_start)
            if elem.date_start < q.date_start:
                # print("Меньше!")
                s_nums.append(elem)
            elif elem.date_start > q.date_start:
                m_nums.append(elem)
                # print("БОЛЬШЕ!")
            else:
                e_nums.append(elem)
        return sort_by_date_start(s_nums) + e_nums + sort_by_date_start(m_nums)

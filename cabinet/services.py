import random
from itertools import chain

from django.db.models import Q

from .models import Car, Driver, AutoDoc, DriverDoc, TypeOfAppl, CarBrand, DocType


class Context():
    '''Получение контекста'''

    def get_car_brands(self):
        return CarBrand.objects.all()

    def get_drivers(self):
        return Driver.objects.all()

    def get_regions(self):
        return Car.objects.all().values('region_code').distinct()

    def get_types_of_app(self):
        return TypeOfAppl.objects.all()

    def get_all_types_of_docs(self):
        return DocType.objects.all()

    def get_all_docs(self):
        auto_doc = AutoDoc.objects.all()
        driver_doc = DriverDoc.objects.all()
        query_set = list(chain(auto_doc, driver_doc))
        # print(query_set)
        def sort_by_date_start(list_to_sort):
            if len(list_to_sort) <= 1:
                return list_to_sort
            else:
                q = random.choice(list_to_sort)
                s_nums = []  # [меньше q]
                m_nums = []  # [больше q]
                e_nums = []  # [q]
                for elem in list_to_sort:
                    print(elem.date_start)
                    if elem.date_start < q.date_start:
                        print("Меньше!")
                        s_nums.append(elem)
                    elif elem.date_start > q.date_start:
                        m_nums.append(elem)
                        print("БОЛЬШЕ!")
                    else:
                        e_nums.append(elem)
                return sort_by_date_start(s_nums) + e_nums + sort_by_date_start(m_nums)

        sorting_queryset = sort_by_date_start(query_set)
        return sorting_queryset



def filtration_car(get_params):
    reg_number = get_params.get('registration_number')
    if reg_number == '': reg_number = '`'

    query_set = Car.objects.filter(
        Q(registration_number__icontains=reg_number) |
        Q(brand__in=get_params.getlist('brand')) |
        Q(owner__in=get_params.getlist('driver')) |
        Q(region_code__in=get_params.getlist('region')) |
        (Q(applications__type_of_id__in=get_params.getlist('type_of_app')) & Q(
            applications__is_active=True))

    )
    return query_set.distinct()


def filtration_driver(get_params):
    """Возвращает отфильтрованный queryset"""
    last_name = get_params.get('last_name')
    phone = get_params.get('phone')

    if last_name == '': last_name = '`'
    if phone == '': phone = '`'

    query_set = Driver.objects.filter(
        Q(user__last_name__icontains=last_name)
        | Q(phone__icontains=phone)
        | (Q(my_apps__type_of_id__in=get_params.getlist('type_of_app')) & Q(
           my_apps__is_active=True))
    )

    return query_set.distinct()

def filtration_document(get_params):
    """Возвращает отфильтрованный queryset модели document"""

    pass

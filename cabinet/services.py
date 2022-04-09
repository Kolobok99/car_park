import random
from datetime import datetime
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

    def get_car_types_of_docs(self):

        return DocType.objects.filter(type='a')

    def get_man_types_of_docs(self):
        return DocType.objects.filter(type='m')

    def get_all_docs(self):
        auto_doc = AutoDoc.objects.all()
        driver_doc = DriverDoc.objects.all()
        query_set = list(chain(auto_doc, driver_doc))

        sorting_list_of_querysets = sort_by_date_start(query_set)
        return sorting_list_of_querysets



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
    start_date = get_params.get('start_date')
    end_date = get_params.get('end_date')

    man_or_car = get_params.getlist('aorm')

    doc_type_car = get_params.getlist('doc_type-car')
    doc_type_man = get_params.getlist('doc_type-man')

    if start_date == '': start_date = None
    if end_date == '': end_date = None

    print('-------starting----------')
    print(f'{start_date=}')
    print(f'{end_date=}')

    print(f'{man_or_car=}')

    print(f'{doc_type_car=}')
    print(f'{doc_type_man=}')


    def get_docs_between_date(model, start_date=None, end_date=None):
        '''Возвращает queryset model с фильтрацией по дате'''
        print(f'{end_date=}')
        if start_date is None:
            query_set = model.objects.filter(
                date_end__lte=end_date
            )
        elif end_date is None:
            query_set = model.objects.filter(
                date_start__gte=start_date
            )
        else:
            query_set = model.objects.filter(
                Q(date_start__gte=start_date)
                & Q(date_end__lte=end_date)
            )
        return query_set

    def get_docs_with_types(model, list_with_type_id: list):
        """Возвращает queryset model с переданными типами"""
        # print("-----SECOND-----------")
        last_query = None
        list_with_type_id = [int(str_id) for str_id in list_with_type_id]
        # print(f"{list_with_type_id=}")
        for type_of_doc_id in list_with_type_id:
            # print(f'{type_of_doc_id=}')
            new_query = model.objects.filter(type__pk=type_of_doc_id)
            # print(f"{new_query=}")
            if last_query is None:
                last_query = new_query
            else:
                last_query = last_query.union(new_query)
        # print(f"END{last_query=}")
        return last_query

    # ТОЛЬКО АВТО:
    if man_or_car[0] == 'car':
        if (start_date is not None) or (end_date is not None):
            car_docs_date = get_docs_between_date(model=AutoDoc, start_date=start_date, end_date=end_date)
            print(f'{car_docs_date=}')
        else:
            car_docs_date = None

        if doc_type_car is not None:
            car_docs_type = get_docs_with_types(model=AutoDoc, list_with_type_id=doc_type_car)
            print(f'{car_docs_type=}')
        else:
            car_docs_type = None

        if car_docs_date is None and car_docs_type is None:
            return AutoDoc.objects.all()
        elif car_docs_date is None:
            return car_docs_type
        elif car_docs_type is None:
            return car_docs_date
        else:
            # print(f"end -> {(car_docs_type & car_docs_date)}")
            # print(f"end -> {(car_docs_type & car_docs_date).first().date_start}")
            return (car_docs_type & car_docs_date)

    #ТОЛЬКО ВОДИТЕЛИ
    # if man_or_car[0] == 'man':
    #     if (start_date is not None) or (end_date is not None):
    #         man_docs_date = get_docs_between_date(model=DriverDoc, start_date=start_date, end_date=end_date)
    #     else:
    #         man_docs_date = None
    #
    #     if doc_type_car is not None:
    #         car_docs_type = get_docs_with_types(model=AutoDoc, **get_params['doc_type-car'])
    #         # print(f'{car_docs_type=}')
    #     else:
    #         car_docs_type = None
    #
    #     if car_docs_date is None and car_docs_type is None:
    #         return AutoDoc.objects.all()
    #     elif car_docs_date is None:
    #         return car_docs_type
    #     elif car_docs_type is None:
    #         return car_docs_date
    #     else:
    #         return car_docs_type | car_docs_date


    # if list(man_or_car) == 2 or list(man_or_car) == 0:
    #     man_docs_date = get_docs_between_date(model=DriverDoc, start_date=start_date, end_date=end_date)
    #     car_docs_date = get_docs_between_date(model=AutoDoc, start_date=start_date, end_date=end_date)
    #
    # elif man_or_car[0] == 'auto':
    #     if get_params['doc_type-car'] == 0:
    #        if start_date is None and end_date is None:
    #            AutoDoc.objects.all()
    # elif man_or_car[0] == 'man':
    #     if get_params['doc_type-man'] == 0:
    #        if start_date is None and end_date is None:
    #            DriverDoc.objects.all()
    #        else:
    #            man_docs_date = get_docs_between_date(model=DriverDoc, start_date=start_date, end_date=end_date)



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
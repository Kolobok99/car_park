from itertools import chain

from django.db.models import Q
from cabinet.models import Car, MyUser, AutoDoc, UserDoc, FuelCard, TypeOfAppl, Application


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

    query_set = MyUser.objects.filter(
        Q(role='d') &
        (Q(last_name__icontains=last_name)
        | Q(phone__icontains=phone)
        | (Q(my_apps__type_of_id__in=get_params.getlist('type_of_app')) & Q(
           my_apps__is_active=True)))
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

    def query_set_with_filters(model, doc_types):
        """Возвращает query_set оотфильтрованной модели"""
        if (start_date is not None) or (end_date is not None):
            docs_date = get_docs_between_date(model=model, start_date=start_date, end_date=end_date)
        else:
            docs_date = None

        if doc_types is not None:
            docs_type = get_docs_with_types(model=model, list_with_type_id=doc_types)
        else:
            docs_type = None

        if docs_date is None and docs_type is None:
            return model.objects.all()
        elif docs_date is None:
            return docs_type
        elif docs_type is None:
            return docs_date
        else:
            return (docs_type & docs_date)
        # if (start_date is not None) or (end_date is not None):
        #     car_docs_date = get_docs_between_date(model=AutoDoc, start_date=start_date, end_date=end_date)
        #     print(f'{car_docs_date=}')
        # else:
        #     car_docs_date = None
        #
        # if doc_type_car is not None:
        #     car_docs_type = get_docs_with_types(model=AutoDoc, list_with_type_id=doc_type_car)
        #     print(f'{car_docs_type=}')
        # else:
        #     car_docs_type = None
        #
        # if car_docs_date is None and car_docs_type is None:
        #     return AutoDoc.objects.all()
        # elif car_docs_date is None:
        #     return car_docs_type
        # elif car_docs_type is None:
        #     return car_docs_date
        # else:
        #     return (car_docs_type & car_docs_date)
    #ТОЛЬКО ДАТА:
    if len(man_or_car) == 0:
        car_docs_date = get_docs_between_date(model=AutoDoc, start_date=start_date, end_date=end_date)
        man_docs_date = get_docs_between_date(model=UserDoc, start_date=start_date, end_date=end_date)

        return list(chain(car_docs_date, man_docs_date))

    # АВТО+ВОДИТЕЛЬ:
    elif len(man_or_car) == 2:
        # ['car','man']
        query_set_cars = query_set_with_filters(model=AutoDoc, doc_types=doc_type_car)
        query_set_mens = query_set_with_filters(model=UserDoc, doc_types=doc_type_man)

        return list(chain(query_set_cars, query_set_mens))

    # ТОЛЬКО АВТО:
    elif man_or_car[0] == 'car':
        return query_set_with_filters(model=AutoDoc, doc_types=doc_type_car)
        # if (start_date is not None) or (end_date is not None):
        #     car_docs_date = get_docs_between_date(model=AutoDoc, start_date=start_date, end_date=end_date)
        #     print(f'{car_docs_date=}')
        # else:
        #     car_docs_date = None
        #
        # if doc_type_car is not None:
        #     car_docs_type = get_docs_with_types(model=AutoDoc, list_with_type_id=doc_type_car)
        #     print(f'{car_docs_type=}')
        # else:
        #     car_docs_type = None
        #
        # if car_docs_date is None and car_docs_type is None:
        #     return AutoDoc.objects.all()
        # elif car_docs_date is None:
        #     return car_docs_type
        # elif car_docs_type is None:
        #     return car_docs_date
        # else:
        #     return (car_docs_type & car_docs_date)

    #ТОЛЬКО ВОДИТЕЛИ
    elif man_or_car[0] == 'man':
        return query_set_with_filters(model=UserDoc, doc_types=doc_type_man)
        # if (start_date is not None) or (end_date is not None):
        #     man_docs_date = get_docs_between_date(model=DriverDoc, start_date=start_date, end_date=end_date)
        # else:
        #     man_docs_date = None
        #
        # if len(doc_type_man) != 0:
        #     man_docs_type = get_docs_with_types(model=DriverDoc, list_with_type_id=doc_type_man)
        #     print(man_docs_type)
        # else:
        #     man_docs_type = None
        #
        # if man_docs_date is None and man_docs_type is None:
        #     print(1)
        #     return DriverDoc.objects.all()
        # elif man_docs_date is None:
        #     print(2)
        #     return man_docs_type
        # elif man_docs_type is None:
        #     print(3)
        #     return man_docs_date
        # else:
        #     print(f'{(man_docs_type & man_docs_date)=}')
        #     return (man_docs_type & man_docs_date)

    #АВТО И ВОДИТЕЛИ

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

def filtration_cards(get_params):
    """Возвращает QuerySet отфильтрованных данных карт"""

    number = get_params.get('number')

    limit_max = get_params.get('limit_max')
    limit_min = get_params.get('limit_min')

    balance_max = get_params.get('balance_max')
    balance_min = get_params.get('balance_min')

    print('-----Start Cards Filtration')
    print(f'{number=}')
    print(f'{limit_max=}')
    print(f'{limit_min=}')
    print(f'{balance_max=}')
    print(f'{balance_min=}')


    if number == '': number = '`'
    if limit_max == '': limit_max = 100000
    if limit_min == '': limit_min = -9999
    if balance_max == '': balance_max = 100000
    if balance_min == '': balance_min = -9999

    querySet = FuelCard.objects.filter(
        Q(number__icontains=number)
        | (Q(limit__gte=limit_min) & Q(limit__lte=limit_max))
        & (Q(balance__gte=balance_min) & Q(balance__lte=balance_max))
    )
    return querySet

def filtration_apps(get_params):
    '''Возвращает отфильтрованный набор заявок'''


    # GET-параметры

    start_date = get_params.get('start_date')
    end_date = get_params.get('end_date')

    urgency_types = get_params.getlist('urgency_types')
    status_types = get_params.getlist('status_types')
    types_of_apps = get_params.getlist('types_of_apps')

    print("----ПОЛУЧЕНЫЕ ПАРАМЕТРЫ------")
    print(f'{start_date=}')
    print(f'{end_date=}')
    print(f'{urgency_types=}')
    print(f'{status_types=}')
    print(f'{types_of_apps=}')

    if start_date == '': start_date = '1999-01-01'
    if end_date == '': end_date = '2050-01-01'
    if len(urgency_types) == 0: urgency_types = [urg[0] for urg in Application.URGENCY_CHOISES]
    if len(status_types) == 0:  status_types = [stat[0] for stat in Application.STATUS_CHOISES]
    if len(types_of_apps) == 0: types_of_apps = TypeOfAppl.objects.all()

    print("----МОДИФИЦИРОВАННЫЕ------")
    print(f'{start_date=}')
    print(f'{end_date=}')
    print(f'{urgency_types=}')
    print(f'{status_types=}')
    print(f'{types_of_apps=}')

    return_set = Application.objects.filter(
          Q(start_date__gte=start_date)
        & Q(end_date__lte=end_date)
        & Q(urgency__in=urgency_types)
        & Q(status__in=status_types)
        & Q(type_of__in=types_of_apps)
    )

    return return_set

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
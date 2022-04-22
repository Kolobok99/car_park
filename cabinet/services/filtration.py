from itertools import chain

import django_filters
from django.db.models import Q, F
from cabinet.models import Car, MyUser, AutoDoc, UserDoc, FuelCard, TypeOfAppl, Application


def refact2_filtration_car(get_params):
    # 1.1)Получить все get-параметры:
    registration_number = get_params.get('registration_number')

    # 1.2) Получить все getlist параметры:
    brand = get_params.getlist('brand')
    region_code = get_params.getlist('region_code')
    applications = get_params.getlist('applications')

    # 1.3) Получить остальные параметры:
    driver_has = get_params.getlist('driver_has')
    # if driver_has == "driver_no":driver_has = False

    query_set = None

    list_of_query = []
    flag = False

    if registration_number != '':
        query_set = Car.objects.filter(registration_number__icontains=registration_number)
        flag = True
    if brand:
        if flag:
            query_set = query_set.filter(brand__in=brand)
        else:
            query_set = Car.objects.filter(brand__in=brand)
            flag = True
    if len(driver_has) != 2:
        print("NO!")
        if driver_has[0] == 'driver_no':
            if flag:
                query_set = query_set.filter(owner__isnull=True)
            else:
                query_set = Car.objects.filter(owner__isnull=True)
                flag = True
        elif driver_has[0] == 'driver_yes':
            if flag:
                query_set = query_set.filter(owner__isnull=False)
            else:
                query_set = Car.objects.filter(owner__isnull=False)
                flag = True

    if region_code:
        if flag:
            query_set = query_set.filter(region_code__in=region_code)
        else:
            query_set = Car.objects.filter(region_code__in=region_code)
            flag = True
    if applications:
        if flag:
            query_set = query_set.filter(applications__is_active=True)
            query_set = query_set.filter(applications__type_of_id__in=applications)
        else:
            query_set = Car.objects.filter(
                (Q(applications__type_of_id__in=applications) & Q(
                    applications__is_active=True)
                 ))
            flag = True
    if query_set:
        return query_set


def refact_filtration_car(get_params):

    # 1.1)Получить все get-параметры:
    registration_number = get_params.get('registration_number')

    # 1.2) Получить все getlist параметры:
    brand = get_params.getlist('brand')
    region_code = get_params.getlist('region_code')
    applications = get_params.getlist('applications')

    # 1.3) Получить остальные параметры:
    driver_has = get_params.get('driver_has')
    # if driver_has == "driver_no":driver_has = False

    list_of_query = []

    if registration_number != '':
        query_registration_number = Car.objects.filter(registration_number__icontains=registration_number)
        list_of_query.append(query_registration_number)
    if brand:
        query_brand = Car.objects.filter(brand__in=brand)
        list_of_query.append(query_brand)
    if region_code:
        query_region_code = Car.objects.filter(region_code__in=region_code)
        list_of_query.append(query_region_code)
    if applications:
        query_applications = Car.objects.filter(
            (Q(applications__type_of_id__in=applications) & Q(
                applications__is_active=True)
        ))
        list_of_query.append(query_applications)
    if driver_has == 'driver_no':
        query_driver_has = Car.objects.filter(
            owner__isnull=True
        )
        list_of_query.append(query_driver_has)
    else:
        query_driver_has = Car.objects.filter(
            owner__isnull=False
        )
        list_of_query.append(query_driver_has)

    if list_of_query:
        queryset = list_of_query[0]
        for query in list_of_query[1:]:
                queryset = queryset & query
    else:
        queryset = Car.objects.all()
    return queryset



def filtration_car(get_params):

    reg_number = get_params.get('registration_number')
    if reg_number == '': reg_number = '`'

    query_set = Car.objects.filter(
        Q(registration_number__icontains=reg_number) &
        Q(brand__in=get_params.getlist('brand')) &
        Q(region_code__in=get_params.getlist('region_code')) &
        (Q(applications__type_of_id__in=get_params.getlist('applications')) & Q(
            applications__is_active=True))

    )
    return query_set

def refact_filtration_driver(get_params):

    # 1.1) Получить get параметры:
    last_name = get_params.get('last_name')
    phone = get_params.get('phone')
    card_balance = get_params.get('card_balance')
    try: card_balance = int(card_balance)
    except: ...

    # 1.2) Получить get-list параметры:
    applications = get_params.getlist('applications')

    list_of_query = []
    drivers = MyUser.objects.filter(role='d')


    if last_name != '':
        query_last_name = drivers.filter(last_name__icontains=last_name)
        list_of_query.append(query_last_name)

    if phone != '':
        query_phone = drivers.filter(phone__icontains=phone)
        list_of_query.append(query_phone)

    if card_balance == 200:
        query_card_balance = drivers.filter(my_cards__balance__lte=card_balance)
        list_of_query.append(query_card_balance)
    elif card_balance == 500:
        query_card_balance = drivers.filter(my_cards__balance__gte=card_balance)
        list_of_query.append(query_card_balance)
    elif card_balance == 1:
        query_card_balance = drivers.filter(my_cards__isnull=True)
        list_of_query.append(query_card_balance)

    if applications:
        query_applications = drivers.filter(
            (Q(my_apps__type_of_id__in=applications) & Q(
                my_apps__is_active=True))
        )
        list_of_query.append(query_applications)
    if list_of_query:
        queryset = list_of_query[0]
        for query in list_of_query[1:]:
                queryset = queryset & query
    else:
        queryset = drivers
    return queryset

def filtration_driver(get_params):
    """Возвращает отфильтрованный queryset"""


    last_name = get_params.get('last_name')
    phone = get_params.get('phone')
    card_balance = get_params.get('card_balance')
    if last_name == '': last_name = '`'
    if phone == '': phone = '`'
    print(card_balance)

    if card_balance == "200":
        query_set_balance = MyUser.objects.filter(
            Q(my_cards__balance__lte=200) &
            Q(role='d')
        )
    elif card_balance == "500":
        query_set_balance = MyUser.objects.filter(
            Q(my_cards__balance__qte=500) &
            Q(role='d')
        )
    elif card_balance == "0":
        query_set_balance = MyUser.objects.filter(
            Q(my_cards__isnull=True) &
            Q(role='d')
        )
        print("YES!")
        print(query_set_balance)
    else:
        query_set_balance = None

    query_set = MyUser.objects.filter(
        Q(role='d') &
        (Q(last_name__icontains=last_name)
        | Q(phone__icontains=phone)
        | (Q(my_apps__type_of_id__in=get_params.getlist('type_of_app')) & Q(
           my_apps__is_active=True)))
    )
    if query_set_balance == None:
        return query_set.distinct()
    else:
        return query_set_balance

def refact_filtration_documents(get_params):
    def get_docs_between_date(model, start_date='', end_date=''):
        '''Возвращает queryset model'и с фильтрацией по дате'''
        print(f'{end_date=}')
        if start_date == '':
            query_set = model.objects.filter(
                date_end__lte=end_date
            )
        elif end_date == '':
            query_set = model.objects.filter(
                date_start__gte=start_date
            )
        else:
            query_set = model.objects.filter(
                Q(date_start__gte=start_date)
                & Q(date_end__lte=end_date)
            )
        return query_set

    # 1.1) Получаем get-параметры

    start_date = get_params.get('start_date')
    end_date = get_params.get('end_date')

    man_or_car = get_params.getlist('aorm')

    doc_type_car = get_params.getlist('doc_type-car')
    doc_type_man = get_params.getlist('doc_type-man')

    list_of_query = []

    # 2.1
    # if start_date != '' or end_date != '':
    #     query_car_docs_between_date = get_docs_between_date(model=Car, start_date=start_date, end_date=end_date)
    #     query_driver_docs_between_date = get_docs_between_date(model=MyUser, start_date=start_date, end_date=end_date)

    if len(man_or_car) == 2:
        ...
        #документы по дате


    elif man_or_car[0] == 'man':
        pass
    elif man_or_car[0] == 'car':
        pass


def filtration_document(get_params):
    """Возвращает отфильтрованный queryset модели document"""

    # 1.1) Получаем get-параметры

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




def refact_filtration_cards(get_params):

    number = get_params.get('number')

    limit_min = get_params.get('limit_min')
    limit_max = get_params.get('limit_max')

    balance_min = get_params.get('balance_min')
    balance_max = get_params.get('balance_max')

    list_of_query = []
    if number != '':
        query_number = FuelCard.objects.filter(number__icontains=number)
        list_of_query.append(query_number)

    if limit_min != '':
        query_limit_min = FuelCard.objects.filter(limit__gte=limit_min)
        list_of_query.append(query_limit_min)
    if limit_max != '':
        query_limit_max = FuelCard.objects.filter(limit__lte=limit_max)
        list_of_query.append(query_limit_max)

    if balance_min != '':
        query_balance_min = FuelCard.objects.filter(balance__gte=balance_min)
        list_of_query.append(query_balance_min)
    if balance_max != '':
        query_balance_max = FuelCard.objects.filter(balance__lte=balance_max)
        list_of_query.append(query_balance_max)

    if list_of_query:
        queryset = list_of_query[0]
        for query in list_of_query[1:]:
                queryset = queryset & query
    else:
        queryset = FuelCard.objects.all()
    return queryset



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



def refact_filtration_apps(get_params):
    ...
    #1) GET-параметры
    start_date = get_params.get('start_date')
    end_date = get_params.get('end_date')

    urgency = get_params.getlist('urgency_types')
    status= get_params.getlist('status_types')
    type_of = get_params.getlist('types_of_apps')

    list_of_query = []

    if start_date != '' or end_date != '':
        query_date = get_query_between_date(model=Application, start_date=start_date, end_date=end_date)
        list_of_query.append(query_date)
    if urgency:
        query_urgency = Application.objects.filter(urgency__in=urgency)
        list_of_query.append(query_urgency)
    if status:
        query_status = Application.objects.filter(status__in=status)
        list_of_query.append(query_status)
    if type_of:
        query_type_of = Application.objects.filter(type_of__in=type_of)
    if list_of_query:
        queryset = list_of_query[0]
        for query in list_of_query[1:]:
            queryset = queryset & query
    else:
        queryset = Application.objects.all()
    return queryset

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

def get_query_between_date(model, start_date="", end_date=""):
    '''Возвращает queryset model с фильтрацией по дате'''
    print(f'{end_date=}')
    if start_date == "":
        query_set = model.objects.filter(
            date_end__lte=end_date
        )
    elif end_date == "":
        query_set = model.objects.filter(
            date_start__gte=start_date
        )
    else:
        query_set = model.objects.filter(
            Q(date_start__gte=start_date)
            & Q(date_end__lte=end_date)
        )
    return query_set
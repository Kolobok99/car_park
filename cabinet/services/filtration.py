import datetime

import pytz
from django.db.models import Q

from cabinet.models import *


def refact3_filtration_car(get_params):
    """
        Возвращает отфильтрованные по get_params (авто)
    """
    # 1.1)Получить все get-параметры:
    registration_number = get_params.get('registration_number')

    # 1.2) Получить все getlist параметры:
    brand = get_params.getlist('brand')
    region_code = get_params.getlist('region_code')
    applications = get_params.getlist('applications')

    # 1.3) Получить остальные параметры:
    driver_has = get_params.getlist('driver_has')
    # if driver_has == "driver_no":driver_has = False
    list_of_Q = []

    if registration_number and registration_number != "":
        reg_number_parameter = 'registration_number__icontains'
        Q_reg_number = Q(**{reg_number_parameter: registration_number})
        list_of_Q.append(Q_reg_number)

    if brand:
       brand_parameter = 'brand__in'
       Q_brand = Q(**{brand_parameter: brand})
       list_of_Q.append(Q_brand)

    if driver_has and len(driver_has) != 2:
        driver_has_parameter = "owner__isnull"
        Q_driver_has = Q(**{driver_has_parameter: not bool(driver_has[0])})
        list_of_Q.append(Q_driver_has)
    if region_code:
        region_code_parameter = "region_code__in"
        Q_region_code = Q(**{region_code_parameter: region_code})
        list_of_Q.append(Q_region_code)
    if applications:
        applications_parameter = "applications__type_id__in"
        Q_applications = Q(**{applications_parameter: applications})
        Q_active_apps = Q(**{"applications__is_active": True})
        list_of_Q.append(Q_applications)
        list_of_Q.append(Q_active_apps)

    return Car.objects.filter(
        *list_of_Q
    ).distinct()

def refact3_filtration_driver(get_params):
    """
        Возвращает отфильтрованные по get_params (водители)
    """
    last_name = get_params.get('last_name')
    phone = get_params.get('phone')
    card_balance = get_params.get('card_balance')
    try:
        card_balance = int(card_balance)
    except:
        ...
    applications = get_params.getlist('applications')

    list_of_Q = []

    drivers = MyUser.objects.filter(role='d')

    if last_name and last_name != '':
        list_of_Q.append(Q(**{"last_name__icontains": last_name}))
    if phone and phone != '':
        list_of_Q.append(Q(**{"phone__icontains":phone}))

    if card_balance and card_balance == 200:
        list_of_Q.append(Q(**{"my_card__balance__lt": card_balance}))
    elif card_balance and card_balance == 500:
        list_of_Q.append(Q(**{"my_card__balance__gte": card_balance}))
    elif card_balance and card_balance == 1:
        list_of_Q.append(Q(**{"my_card__balance__isnull": True}))

    if applications and applications:
        list_of_Q.append(Q(**{"my_apps__type_id__in": applications}))
        list_of_Q.append(Q(**{"my_apps__is_active": True}))

    return drivers.filter(
        *list_of_Q
    ).distinct()

def refact3_filtration_cards(get_params):
    """
        Возвращает отфильтрованные по get_params (топливные карты)
    """
    print("YES")
    number = get_params.get('number')
    owner = get_params.getlist('owner')

    limit_min = get_params.get('limit_min')
    limit_max = get_params.get('limit_max')

    balance_min = get_params.get('balance_min')
    balance_max = get_params.get('balance_max')

    list_of_Q = []
    # list_of_Q.append(Q(**{"":}))
    if number != '':
        list_of_Q.append(Q(**{"number__icontains": number}))

    if len(owner) != 2:
        owner_parameter = "owner__isnull"
        Q_owner = Q(**{owner_parameter: not bool(owner[0])})
        list_of_Q.append(Q_owner)
    print(type(limit_min))
    if limit_min != '':
        list_of_Q.append(Q(**{"limit__gte": limit_min}))

    if limit_max != '':
        list_of_Q.append(Q(**{"limit__lte": limit_max}))

    if balance_min != '':
        list_of_Q.append(Q(**{"balance__gte": balance_min}))
    if balance_max != '':
        list_of_Q.append(Q(**{"balance__lte": balance_max}))

    return FuelCard.objects.filter(
        *list_of_Q
    ).distinct()

def refact3_filtration_apps(get_params):
    """
        Возвращает отфильтрованные по get_params (активные заявки)
    """
    start_date = get_params.get('start_date')
    end_date = get_params.get('end_date')

    urgency = get_params.getlist('urgency_types')
    status = get_params.getlist('status_types')
    type_of = get_params.getlist('types_of_apps')

    list_of_Q = []
    # list_of_Q.append(Q(**{"":}))
    active_applications = Application.objects.filter(is_active=True)
    if start_date != '':
        list_of_Q.append(Q(**{"start_date__gte": start_date}))
    if end_date != '':
        list_of_Q.append(Q(**{"end_date__lte": end_date}))

    if urgency:
        list_of_Q.append(Q(**{"urgency__in": urgency}))

    if status:
        list_of_Q.append(Q(**{"status__in": status}))

    if type_of:
        list_of_Q.append(Q(**{"type__in":type_of}))


    return active_applications.filter(
        *list_of_Q
    ).distinct()

def refact3_filtration_documents(model, get_params):
    """
        Возвращает отфильтрованные по get_params (документы)
    """

    start_date = get_params.get('start_date')
    end_date = get_params.get('end_date')

    doc_type = get_params.getlist('doc_type')

    list_of_Q = []

    if start_date != '':
        list_of_Q.append(Q(**{"start_date__gte": start_date}))
    if end_date != '':
        list_of_Q.append(Q(**{"end_date__lte": end_date}))
    if doc_type:
        # list_with_type_id = [int(str_id) for str_id in doc_type]
        list_of_Q.append(Q(**{"type__in": doc_type}))

    return model.objects.filter(
        *list_of_Q
    ).distinct()


def filtration_logs(list_with_logs, get_params):
    """
        Возвращает отфильтрованный список по get_params (все логи)
    """

    log_status = get_params.getlist('log_status')
    log_type = get_params.getlist('log_type')
    log_time = get_params.get('log_time')

    return_status = []
    return_type = []
    return_time = []

    if log_status:
        for l in list_with_logs:
            for s in log_status:
                if l[0].history_type == s:
                    return_status.append(l)
    if log_type:
        for l in list_with_logs:
            for t in log_type:
                if str(l[0].__class__)[33:-2] == t:
                    return_type.append(l)
    if log_time:
        for l in list_with_logs:
            today = datetime.datetime.now()
            today = pytz.utc.localize(today)
            filter_date = today - timedelta(days=int(log_time))
            if l[0].history_date > filter_date:
                return_time.append(l)


    if log_type and log_status and log_type:
        ret = [l for l in return_status if l in return_type and l in return_time]
        return ret

    elif log_type and log_status:
        ret = [l for l in return_status if l in return_type]
        return ret
    elif log_type and log_time:
        ret = [l for l in return_time if l in return_type]
        return ret
    elif log_time and log_status:
        ret = [l for l in return_status if l in return_time]
        return ret

    elif log_status:
        return return_status
    elif log_type:
        return return_type
    elif log_time:
        return return_time



from django.db.models import Q

from .models import Car, Driver


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
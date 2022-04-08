from django.db.models import Q

from .models import Car

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
    return query_set
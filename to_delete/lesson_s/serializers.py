from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

# LESSON 1
from cabinet.models import CarBrand, Car

"""
from rest_framework import serializers
from cabinet.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('registration_number',
                  'brand_id',)
"""
# LESSON 3
"""

"""
# LESSON 3
"""
# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
# django.setup()

# LESSON 4
import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from cabinet.models import Car



class CarModel:
    def __init__(self, reg_number, brand_id):
        self.reg_number = reg_number
        self.brand_id = brand_id

class CarSerializer(serializers.Serializer):
    reg_number = serializers.CharField(max_length=6)
    brand_id = serializers.IntegerField()


def encode():
    
    model = CarModel('A123AA', 3)
    # преобразование данных модели в словарь
    # {'reg_number': 'A123AA', 'brand_id': 3}
    model_sr = CarSerializer(model)
    print(model_sr.data, type(model_sr.data), sep='\n')

    # преобразование словаря в json byte строку
    # b'{"reg_number":"A123AA","brand_id":3}'
    json = JSONRenderer().render(model_sr.data)
    print(f"{json=}")

def decode():
    'JSON ---> CarModel'

    stream = io.BytesIO(b'{"reg_number":"A123AA","brand_id":3}')

    # json b'строка' -> dict()
    # {'reg_number': 'A123AA', 'brand_id': 3}
    data = JSONParser().parse(stream)
    print(f"{data=}")

    serializer = CarSerializer(data=data)
    serializer.is_valid()
    print(f"{serializer.validated_data=}")

"""
# lESSON 4
"""
class CarBrandSerializer(serializers.Serializer):
    "Сериалайзер Марок"

    title = serializers.CharField(max_length=20, label='Марки')
"""

# LESSON 5
"""
class CarBrandSerializer(serializers.Serializer):
    "Сериалайзер Марок"

    title = serializers.CharField(max_length=20, label='Марки')

    def create(self, validated_data):
        return CarBrand.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
"""
# LESSON 6
"""
"""
class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('pk',
                  'registration_number',
                  'brand',
                 )
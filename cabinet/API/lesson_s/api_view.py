from rest_framework.response import Response
from rest_framework.views import APIView

from cabinet.API.lesson_s.serializers import CarSerializer
from cabinet.models import CarBrand, Car

# LESSON 1
"""
from cabinet.API.lesson2.serializers import CarSerializer
from cabinet.models import Car
from rest_framework import generics

class CarAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
"""
# LESSON 2
"""
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from cabinet.models import Car, CarBrand
from rest_framework import generics

class CarAPIView(APIView):

    def get(self, request):
        return Response({'reg_number': 'A123AA'})

    def post(self, request):
        new_brand =CarBrand.objects.create(
            title=request.data['title']
        )
        return Response({'post': model_to_dict(new_brand)})
"""
# LESSON 3
"""
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from cabinet.models import Car, CarBrand
from rest_framework import generics

class CarAPIView(APIView):

    def get(self, request):
        return Response({'reg_number': 'A123AA'})

    def post(self, request):
        new_brand =CarBrand.objects.create(
            title=request.data['title']
        )
        return Response({'post': model_to_dict(new_brand)})
"""

# LESSON 4
"""
class BrandAPIView(APIView):

    def get(self, request):
        brands = CarBrand.objects.all()
        data = CarBrandSerializer(brands, many=True).data
        return Response({"posts": data})

    def post(self, request):
        serializer = CarBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_brand = CarBrand.objects.create(
            title=request.data['title']
        )
        return Response({"post": CarBrandSerializer(new_brand).data})
"""

# LESSON 6
"""
class BrandAPIView(APIView):

    def get(self, request):
        brands = CarBrand.objects.all()
        data = CarBrandSerializer(brands, many=True).data
        return Response({"posts": data})

    def post(self, request):
        serializer = CarBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def put(self, reqeust, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Error pk!"})

        try:
            instance = CarBrand.objects.get(pk=pk)
        except:
            return Response({"error": "Not found Brand by pk"})\

        serializer = CarBrandSerializer(data=reqeust.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data}) 
"""

# LESSON 7
"""
"""
class CarAPIView(APIView):

    def get(self, request):
        cars = Car.objects.all()
        data = CarSerializer(cars, many=True).data
        return Response({"posts": data})

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def put(self, reqeust, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Error pk!"})

        try:
            instance = Car.objects.get(pk=pk)
        except:
            return Response({"error": "Not found Brand by pk"})

        serializer = CarSerializer(data=reqeust.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})


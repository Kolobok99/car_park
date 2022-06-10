from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from cabinet.API.serializers import CarSerializer, CarCreateSerializer, DriverSerializer, AutoDocsSerializer, \
    UserDocsSerializer, FuelCardSerializer, ApplicationSerializer, RegistrationSerializer
from cabinet.models import Car, MyUser, AutoDoc, UserDoc, FuelCard, Application
from cabinet.services.filtration import refact3_filtration_car, refact3_filtration_driver, refact3_filtration_documents, \
    refact3_filtration_cards, refact3_filtration_apps

from cabinet.services.services import Context


class CarAPIViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'registration_number'

    def filtration(self, request):
        """
        :param:
        ?
        registration_number=
        brand=3
        driver_has=

        """
        if len(request.GET) == 0:
            queryset = self.get_queryset()
        else:
            queryset = refact3_filtration_car(request.GET)
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data)

    def owner_none(self, request, *args, **kwargs):
        """
        Удаляет владельца у переданного списка машин
        """
        action = request.data.get('action')
        car_id = request.data.get('owner_refuse_id')
        # &action=owner-none&owner_refuse_id=5&owner_refuse_id=7
        if action == 'owner_none':
            none_owner_pk = request.data.get('owner_refuse_id')
            print(f"{none_owner_pk=}")
            # none_owner_pk=['5', '7']
            cars_none = Car.objects.filter(pk__in=none_owner_pk)
            print(f"{cars_none=}")
            for car in cars_none:
                car.owner = None
                car.save()
            return Response({"posts": "Машины изъяты!"})
        else:
            return Response({"error": "Некорректный формат"})

    def list_to_delete(self, request, *args, **kwargs):
        """ Удаляет список машин  """
        action = request.data.get('action')
        # &action=owner-none&owner_refuse_id=5&owner_refuse_id=7
        if action == 'delete_cars':
            delete_cars_pk = request.data.get('owner_refuse_id')
            cars_none = Car.objects.filter(pk__in=delete_cars_pk).delete()
            return Response({"posts": "Машины изъяты!"})
        else:
            return Response({"error": "Некорректный формат"})


class DriverAPIViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(role='d')
    serializer_class = DriverSerializer

    def filtration(self, request):
        """
        :param:
        ?
        last_name=
        &phone=
        &applications=
        &card_balance=

        """
        if len(request.GET) == 0:
            queryset = self.get_queryset()
        else:
            queryset = refact3_filtration_driver(request.GET)
        serializer = DriverSerializer(queryset, many=True)
        return Response(serializer.data)


# class AllDocsAPIViewSet(ViewSet):
#
#       def list(self, request):
#

class AutoDocsAPIViewSet(ModelViewSet):
    queryset = AutoDoc.objects.all()
    serializer_class = AutoDocsSerializer

    def filtration(self, request):
        """
        :param:
        ?
        last_name=
        &phone=
        &applications=
        &card_balance=

        """
        if len(request.GET) == 0:
            queryset = self.get_queryset()
        else:
            queryset = refact3_filtration_documents(request.GET)
        serializer = AutoDocsSerializer(queryset, many=True)
        return Response(serializer.data)


class DriverDocsAPIViewSet(ModelViewSet):
    queryset = UserDoc.objects.all()
    serializer_class = UserDocsSerializer

    def filtration(self, request):
        """
        :param:
        ?
        last_name=
        &phone=
        &applications=
        &card_balance=

        """
        if len(request.GET) == 0:
            queryset = self.get_queryset()
        else:
            queryset = refact3_filtration_documents(request.GET)
        serializer = UserDocsSerializer(queryset, many=True)
        return Response(serializer.data)

class CardsAPIViewSet(ModelViewSet):
    queryset = FuelCard.objects.all()
    serializer_class = FuelCardSerializer

    def filtration(self, request):
        """
        :param:
        ?
        last_name=
        &phone=
        &applications=
        &card_balance=

        """
        if len(request.GET) == 0:
            queryset = self.get_queryset()
        else:
            queryset = refact3_filtration_cards(request.GET)
        serializer = FuelCardSerializer(queryset, many=True)
        return Response(serializer.data)

    def owner_none(self, request, *args, **kwargs):
        """
        Удаляет владельца у переданного списка карт
        """
        action = request.data.get('action')

        # &action=owner-none&owner_refuse_id=5&owner_refuse_id=7
        if action == 'owner_none':
            none_owner_pk = request.data.get('owner_refuse_id')
            cards_none = Car.objects.filter(pk__in=none_owner_pk).update()
            return Response({"posts": "Машины изъяты!"})
        else:
            return Response({"error": "Некорректный формат"})

    def list_to_delete(self, request, *args, **kwargs):
        """ Удаляет список машин  """
        action = request.data.get('action')
        if action == 'delete_cards':
            delete_cards_pk = request.data.get('owner_refuse_id')
            cars_none = Car.objects.filter(pk__in=delete_cards_pk).delete()
            return Response({"posts": "Машины изъяты!"})
        else:
            return Response({"error": "Некорректный формат"})

class ApplicationsPIViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def filtration(self, request):
        """
        :param:
        ?
        last_name=
        &phone=
        &applications=
        &card_balance=

        """
        if len(request.GET) == 0:
            queryset = self.get_queryset()
        else:
            queryset = refact3_filtration_apps(request.GET)
        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data)


class HistoryAPIViewSet(Context, ViewSet):

    def list(self, request):
        all_logs = self.get_all_history()
        return Response(all_logs)


# Создаём класс RegistrUserView
class UserAPIViewSet(ModelViewSet):
    # Добавляем в queryset
    queryset = MyUser.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = RegistrationSerializer
    # Добавляем права доступа
    # permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def create(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = RegistrationSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)
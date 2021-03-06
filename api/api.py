from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from api import permissions
from api.serializers import CarSerializer, DriverSerializer, AutoDocsSerializer, \
    UserDocsSerializer, FuelCardSerializer, ApplicationSerializer, RegistrationSerializer
from cabinet.models import Car, MyUser, AutoDoc, UserDoc, FuelCard, Application
from cabinet.services.filtration import filtration_car, filtration_driver, filtration_documents, \
    filtration_cards, filtration_apps

from cabinet.services.services import Context


class CarAPIViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'registration_number'

    def get_permissions(self):
        action = self.action
        print(action)
        if action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsManagerOrOwner]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super(CarAPIViewSet, self).get_permissions()
    # @decorators.action(permission_classes=(permissions.IsManagerOrOwner, ))

    @action(methods=['get'], detail=False)
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
            queryset = filtration_car(request.GET)
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail='False')
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

    @action(methods=['post'], detail='False')
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


    def get_permissions(self):
        action = self.action
        print(action)
        if action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsStaffOrThisUser]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()

    @action(methods=['get'], detail='False')
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
            queryset = filtration_driver(request.GET)
        serializer = DriverSerializer(queryset, many=True)
        return Response(serializer.data)


# class AllDocsAPIViewSet(ViewSet):
#
#       def list(self, request):
#

class AutoDocsAPIViewSet(ModelViewSet):
    queryset = AutoDoc.objects.all()
    serializer_class = AutoDocsSerializer

    def get_permissions(self):
        action = self.action
        print(action)
        if action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsManagerOrOwner]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()

    @action(methods=['get'], detail='False')
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
            queryset = filtration_documents(request.GET, )
        serializer = AutoDocsSerializer(queryset, many=True)
        return Response(serializer.data)


class DriverDocsAPIViewSet(ModelViewSet):
    queryset = UserDoc.objects.all()
    serializer_class = UserDocsSerializer

    def get_permissions(self):
        action = self.action
        print(action)
        if action in ['retrieve', 'destroy']:
            self.permission_classes = [permissions.IsManagerOrOwner]
        if action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsOwnerOnly]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()

    @action(methods=['get'], detail='False')
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
            queryset = filtration_documents(request.GET, )
        serializer = UserDocsSerializer(queryset, many=True)
        return Response(serializer.data)

class CardsAPIViewSet(ModelViewSet):
    queryset = FuelCard.objects.all()
    serializer_class = FuelCardSerializer
    lookup_field = 'number'
    def get_permissions(self):
        action = self.action
        # print(action)
        if action in ['retrieve', 'partial_update', 'destroy',]:
            self.permission_classes = [permissions.IsManagerOrOwner, ]
        # else:
        #     self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()

    @action(methods=['get'], detail='False')
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
            queryset = filtration_cards(request.GET)
        serializer = FuelCardSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail='False')
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

    @action(methods=['post'], detail='False')
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

    def get_permissions(self):
        action = self.action
        user = self.request.user
        if action in ['retrieve', 'update', 'create']:
            self.permission_classes = [permissions.IsManagerOrOwner]
        else:
            self.permission_classes = [permissions.IsOwnerOnly]

        return super().get_permissions()

    @action(methods=['get'], detail='False')
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
            queryset = filtration_apps(request.GET)
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
    @action(methods=['post'], detail='False')
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
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from app.mixins import MultipleSerializerMixin, EnablePartialUpdateMixin
from app.serializers import (
    UsersListeSerializer, UsersDetailsSerializer,
    ColonnesListeSerializer,
    TachesListeSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from app.models import (
    Colonne,
    Tache
)

class ReadUpdateModelViewSet(ModelViewSet):
    http_method_names = ["get", "put", "patch"]

class CreateModelViewSet(ModelViewSet):
    http_method_names = ["post"]

class CRUModelViewSet(ModelViewSet):
    http_method_names = ["get", "put", "patch", "post"]

# class UsersAPIViewset(MultipleSerializerMixin, ModelViewSet):
# class UsersAPIViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
class UsersAPIViewset(MultipleSerializerMixin, ReadUpdateModelViewSet):
# class UsersAPIViewset(MultipleSerializerMixin, ReadUpdateModelViewSet, EnablePartialUpdateMixin):
    serializer_class = UsersListeSerializer
    details_serializer_class = UsersDetailsSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["deactivate", "activate"]:
            self.permission_classes = [IsAuthenticated,]
        elif self.action in ["retrieve"]:
            self.permission_classes = [IsAuthenticatedOrReadOnly,]

        return super().get_permissions()

    def get_queryset(self):
        queryset = User.objects.all()

        return queryset

    # @action(detail=True, methods=["patch"], permission_classes = [IsAuthenticated])
    @action(detail=True, methods=["patch"])
    def deactivate(self, request, pk):
        self.get_object().deactivate()

        return Response()

    # @action(detail=True, methods=["patch"],  permission_classes = [IsAuthenticated])
    @action(detail=True, methods=["patch"])
    def activate(self, request, pk):
        self.get_object().activate()

        return Response()

class ColonnesAPIViewset(MultipleSerializerMixin, CRUModelViewSet, EnablePartialUpdateMixin):
    serializer_class = ColonnesListeSerializer

    def get_queryset(self):
        queryset = Colonne.objects.all()

        return queryset

    # @action(detail=True, methods=["patch"], permission_classes = [AllowAny])
    # def move(self, request, pk):
    #     received_data = request.data
    #     colonne = Colonne.objects.get(pk=pk)
    #     old_position = colonne.position_colonne
    #     new_position = int(received_data["position_colonne"])

    #     self.get_object().move(old_position, new_position)
    #     # print("backward move") if old_position > new_position else print("forward move")

    #     return Response()

class TachesAPIViewset(MultipleSerializerMixin, CRUModelViewSet, EnablePartialUpdateMixin):
    serializer_class = TachesListeSerializer

    def get_queryset(self):
        queryset = Tache.objects.all()

        return queryset

    # @action(detail=True, methods=["patch"], permission_classes = [AllowAny])
    # def move(self, request, pk):
    #     received_data = request.data

    #     self.get_object().move()
    #     print(received_data)

    #     return Response()

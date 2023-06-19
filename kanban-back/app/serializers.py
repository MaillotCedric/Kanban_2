from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from app.models import (
    Colonne,
    Tache
)

class UsersListeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active"]

class UsersDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class TachesListeSerializer(ModelSerializer):
    class Meta:
        model = Tache
        fields = ["id_tache", "titre_tache", "position_tache", "colonne"]

class TachesListeConciseSerializer(ModelSerializer):
    class Meta:
        model = Tache
        fields = ["id_tache", "titre_tache", "position_tache"]

class ColonnesListeSerializer(ModelSerializer):
    taches = SerializerMethodField()

    class Meta:
        model = Colonne
        fields = ["id_colonne", "titre_colonne", "position_colonne", "taches"]

    def get_taches(self, instance):
        queryset = instance.taches
        serializer = TachesListeConciseSerializer(queryset, many=True)

        return serializer.data

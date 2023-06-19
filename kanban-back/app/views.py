from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Colonne, Tache
import app.toolbox as tb
import json

@login_required(login_url="login")
def home(request):
    return render(request, "home.html", {})

def login_(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect("home")
        else:
            messages.warning(request, "Username and/or password not valid")

            return redirect("login")
    else:
        return render(request, "login.html", {})

def logout_(request):
    logout(request)
    messages.success(request, "Logged out")

    return redirect("login")

class PredictAPIView(APIView):
    ''' POST request
    def post(self, *args, **kwargs):
        ...
    '''

    def get(self, *args, **kwargs):
        data = {
            "price": 12345
        }

        return Response(data)

class ColonneMoveView(APIView):
    @transaction.atomic
    def patch(self, *args, **kwargs):
        request = args[0]
        received_data = request.data
        pk = received_data["id_colonne"]
        colonne = Colonne.objects.get(pk=pk)
        old_position = colonne.position_colonne
        new_position = int(received_data["position_colonne"])

        tb.space_move("colonne", colonne, old_position, new_position)

        colonne_object = json.loads(serializers.serialize("json", Colonne.objects.filter(pk=pk)))
        fields = colonne_object[0]["fields"]

        return Response(fields)

class TacheMoveView(APIView):
    @transaction.atomic
    def patch(self, *args, **kwargs):
        request = args[0]
        received_data = request.data
        pk = received_data["id_tache"]
        tache = Tache.objects.get(pk=pk)
        old_tache_position = tache.position_tache
        new_tache_position = int(received_data["position_tache"])
        old_column = tache.colonne
        old_column_position = old_column.position_colonne
        new_column_position = int(received_data["colonne"])
        new_colonne = Colonne.objects.get(id_colonne = new_column_position)

        if new_column_position == old_column_position:
            tb.space_move("tache", tache, old_tache_position, new_tache_position)
        else:
            tb.space_time_move(tache, old_column, new_colonne, old_tache_position, new_tache_position)

        tache_object = json.loads(serializers.serialize("json", Tache.objects.filter(pk=pk)))
        fields = tache_object[0]["fields"]

        return Response(fields)

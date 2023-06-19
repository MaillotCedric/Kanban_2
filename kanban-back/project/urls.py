"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from app.viewsets import (
    UsersAPIViewset,
    ColonnesAPIViewset,
    TachesAPIViewset
)
from app.views import (
    login_,
    PredictAPIView,
    ColonneMoveView,
    TacheMoveView
)

router = routers.SimpleRouter()

router.register("users", UsersAPIViewset, basename="users")
router.register("colonnes", ColonnesAPIViewset, basename="colonnes")
router.register("taches", TachesAPIViewset, basename="taches")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app.urls")),
    path("api/", include(router.urls)),
    path("api/predict/", PredictAPIView.as_view()),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/colonne/move/", ColonneMoveView.as_view(), name="colonne_move"),
    path("api/tache/move/", TacheMoveView.as_view(), name="tache_move"),
    # path("login/", login_, name="login"),
]

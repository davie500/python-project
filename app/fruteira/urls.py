from django.urls import path

from . import views

app_name = "fruteira"

urlpatterns = [
    path("", views.fruteira_home, name="home"),
]

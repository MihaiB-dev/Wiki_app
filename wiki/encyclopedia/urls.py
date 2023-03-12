from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.Search, name ="search"),
    path("create_new_page", views.Create, name="create"),
    path("wiki/<str:title>/edit_page",views.Edit, name="edit"),
    path("random_page",views.Random_page, name="random")
]

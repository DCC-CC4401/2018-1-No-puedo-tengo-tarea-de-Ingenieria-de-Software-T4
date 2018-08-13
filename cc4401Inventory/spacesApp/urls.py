from django.urls import path

from . import views

urlpatterns = [
    path('<int:space_id>/delete', views.space_delete, name='space_delete'),
]

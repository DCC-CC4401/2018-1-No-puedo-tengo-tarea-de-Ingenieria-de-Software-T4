from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_articles),
    path('articles/', views.landing_articles, name='landing_articles'),
    path('spaces/', views.landing_spaces, name='landing_spaces'),
    path('spaces/newReservation', views.new_reservation, name='msg_nueva_reserva'),
    path('search/', views.search, name='search'),
]

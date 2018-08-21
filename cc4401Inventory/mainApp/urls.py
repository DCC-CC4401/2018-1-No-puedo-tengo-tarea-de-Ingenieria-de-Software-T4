from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_articles),
    path('articles/', views.landing_articles, name='landing_articles'),
    path('spaces/', views.landing_spaces, name='landing_spaces'),
    path('spaces/newReservation', views.new_reservation, name='msg_nueva_reserva'),
    path('filtro/newReservation', views.new_reservation, name='msg_nueva_reserva'),
    path('spaces/makeReservation', views.make_reservation, name='do_reservar'),
    path('filtro/makeReservation', views.make_reservation, name='do_reservar'),
    path('search/', views.search, name='search'),
    path('filtro/', views.filtro_spaces, name='filtro_spaces'),
    path('spaces/',views.get_date, name='get_date'),

]

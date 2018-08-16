from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.delete_reservation, name='delete_reservation'),
    path('<int:Reservation_id>', views.reservation_data, name='reservation_data')
]

from django.urls import path

from . import views
import mainApp

urlpatterns = [
    path('<int:space_id>/delete', views.space_delete, name='space_delete'),
    path('<int:space_id>', views.space_data, name='space_data'),
    path('<int:space_id>/edit_name', views.space_edit_name, name='space_edit_name'),
    path('<int:space_id>/edit_capacity', views.space_edit_capacity, name='space_edit_capacity'),
    path('<int:space_id>/edit_image', views.space_edit_image, name='space_edit_image'),
    path('<int:space_id>/edit_description', views.space_edit_description, name='space_edit_description'),
    path('newReservation', mainApp.views.new_reservation, name='msg_nueva_reserva'),
    path('makeReservation', mainApp.views.make_reservation, name='do_reserva'),
]

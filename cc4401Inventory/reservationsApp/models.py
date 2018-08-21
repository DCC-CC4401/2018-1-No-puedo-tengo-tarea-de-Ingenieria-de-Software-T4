from mainApp.models import Action
from spacesApp.models import Space
from django.db import models


class Reservation(Action):

    RESERVATIONSTATES = (
        ('P', 'Pendiente'),
        ('V', 'Vigente'),
        ('R', 'Rechazado')

    )
    reservation_state = models.CharField('Estado Reserva', choices=RESERVATIONSTATES, max_length=1, default='E')
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

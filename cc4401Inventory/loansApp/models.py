from mainApp.models import Action
from articlesApp.models import Article
from django.db import models


class Loan(Action):

    LOANSTATES = (
        ('E', 'En revisión'),
        ('V', 'Vigente'),
        ('C', 'Caducado'),
        ('P', 'Perdido'),
        ('R', 'Recibido')
    )
    loan_state = models.CharField('Estado Prestamo', choices=LOANSTATES, max_length=1, default='E')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

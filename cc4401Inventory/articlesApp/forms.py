from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:

        model = Article
        fields = ['name', 'description', 'image', 'state']

"""
STATES = (
        ('D', 'Disponible'),
        ('P', 'En préstamo'),
        ('R', 'En reparación'),
        ('L', 'Perdido')
    )
    name = forms.CharField(label='Nombre', max_length=40, required=True)
    description = forms.CharField(label='Descripción', required=True)
    image = forms.ImageField(label='Imagen del articulo')
    state = forms.ChoiceField(label='Estado', choices=STATES, required=True)
  
"""

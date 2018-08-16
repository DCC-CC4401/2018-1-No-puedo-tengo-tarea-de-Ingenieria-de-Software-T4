from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articlesApp.models import Article
from spacesApp.models import Space
from django.contrib import messages
# Create your views here.

@login_required
def space_delete(request, space_id):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:
            space = Space.objects.get(id=space_id)
            space.delete()
            messages.success(request, 'Espacio eliminado')
            articles = Article.objects.all()
            spaces = Space.objects.all()
            context = {
                'articles': articles,
                'spaces': spaces
            }
            return render(request, 'items_panel.html', context)
        except:
            return redirect('/')

@login_required
def space_data(request, space_id):
    try:
        space = Space.objects.get(id=space_id)
        context = {
            'space': space
        }
        return render(request, 'spacesApp/space_data.html', context)
    except Exception as ex:
        print('Exception in space_data.')
        print(ex)
        return redirect('/')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articlesApp.models import Article
from spacesApp.models import Space
from django.contrib import messages
import os
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
            'space': space,
            'user_is_staff': request.user.is_staff
        }
        return render(request, 'spacesApp/space_data.html', context)
    except Exception as ex:
        print('Exception in space_data.')
        print(ex)
        return redirect('/')

@login_required
def space_edit_name(request, space_id):

    if request.user.is_staff and request.method == "POST":
        s = Space.objects.get(id=space_id)
        s.name = request.POST["name"]
        s.save()
    return redirect('/space/'+str(space_id))


@login_required
def space_edit_capacity(request, space_id):

    if request.user.is_staff and request.method == "POST":
        s = Space.objects.get(id=space_id)
        try:
            s.capacity = int(request.POST["capacity"])
            s.save()
        except ValueError as ve:
            print('Value error in space_edit_capacity\n'+ve)
    return redirect('/space/' + str(space_id))

@login_required
def space_edit_image(request, space_id):

    if request.user.is_staff and request.method == "POST":
        u_file = request.FILES["image"]
        extension = os.path.splitext(u_file.name)[1]
        s = Space.objects.get(id=space_id)
        s.image.save(str(space_id)+"_space_image"+extension, u_file)
        s.save()
    return redirect('/space/' + str(space_id))


@login_required
def space_edit_description(request, space_id):
    if request.user.is_staff and request.method == "POST":
        s = Space.objects.get(id=space_id)
        s.description = request.POST["description"]
        s.save()
    return redirect('/space/' + str(space_id))

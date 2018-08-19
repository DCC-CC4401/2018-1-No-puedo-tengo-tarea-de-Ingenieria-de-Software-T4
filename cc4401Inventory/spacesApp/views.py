from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.db.models.functions import Lower
import datetime
from articlesApp.models import Article
from spacesApp.models import Space
from reservationsApp.models import Reservation
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
def space_data(request, space_id, date=None):
    try:
        space = Space.objects.get(id=space_id)
        spaces = Space.objects.all().order_by(Lower('name'))

        if date:
            current_date = date
            current_week = datetime.datetime.strptime(current_date, "%Y-%m-%d").date().isocalendar()[1]
        else:
            try:
                current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
                current_date = request.GET["date"]
            except:
                current_week = datetime.date.today().isocalendar()[1]
                current_date = datetime.date.today().strftime("%Y-%m-%d")

        reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'],
                                                  space__name=space.name)

        colores = {'A': 'rgba(0,153,0,0.7)',
                   'P': 'rgba(51,51,204,0.7)'}

        res_list = []
        for i in range(5):
            res_list.append(list())
        for r in reservations:
            reserv = []
            reserv.append(r.space.name)
            reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
            reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
            reserv.append(colores[r.state])
            res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

        move_controls = list()
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-4)).strftime("%Y-%m-%d"))
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d"))
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=4)).strftime("%Y-%m-%d"))

        delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
        monday = (
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime(
                "%d/%m/%Y"))
        tuesday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta - 1)).strftime(
            "%d/%m/%Y"))
        wednesday = (
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta - 2)).strftime(
                "%d/%m/%Y"))
        thursday = (
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta - 3)).strftime(
                "%d/%m/%Y"))
        friday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta - 4)).strftime(
            "%d/%m/%Y"))

        context = {
            'space': space,
            'user_is_staff': request.user.is_staff,
            'reservations': res_list,
            'current_date': current_date,
            'controls': move_controls,
            'actual_monday': monday,
            'actual_tuesday': tuesday,
            'actual_wednesday': wednesday,
            'actual_thursday': thursday,
            'actual_friday': friday,
            'espacios_filtrados': [space.name],
            'espacios': spaces
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
    return redirect('/space/' + str(space_id))


@login_required
def space_edit_capacity(request, space_id):
    if request.user.is_staff and request.method == "POST":
        s = Space.objects.get(id=space_id)
        try:
            s.capacity = int(request.POST["capacity"])
            s.save()
        except ValueError as ve:
            print('Value error in space_edit_capacity\n' + ve)
    return redirect('/space/' + str(space_id))


@login_required
def space_edit_image(request, space_id):
    if request.user.is_staff and request.method == "POST":
        u_file = request.FILES["image"]
        extension = os.path.splitext(u_file.name)[1]
        s = Space.objects.get(id=space_id)
        s.image.save(str(space_id) + "_space_image" + extension, u_file)
        s.save()
    return redirect('/space/' + str(space_id))


@login_required
def space_edit_description(request, space_id):
    if request.user.is_staff and request.method == "POST":
        s = Space.objects.get(id=space_id)
        s.description = request.POST["description"]
        s.save()
    return redirect('/space/' + str(space_id))


from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import localtime
from django.db.models.functions import Lower
import datetime
from spacesApp.models import Space
from articlesApp.models import Article
from reservationsApp.models import Reservation
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def landing_articles(request):
    context = {}
    return render(request, 'articulos.html', context)


@login_required
def landing_spaces(request, date=None, espacios_filtrados=[]):
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

    if not espacios_filtrados:
        reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'])

    else:
        reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'],
                                                  space__name__in=espacios_filtrados)

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
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%d/%m/%Y"))
    tuesday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta-1)).strftime("%d/%m/%Y"))
    wednesday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta-2)).strftime("%d/%m/%Y"))
    thursday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta-3)).strftime("%d/%m/%Y"))
    friday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta-4)).strftime("%d/%m/%Y"))
    context = {'reservations': res_list,
               'current_date': current_date,
               'controls': move_controls,
               'actual_monday': monday,
               'actual_tuesday': tuesday,
               'actual_wednesday': wednesday,
               'actual_thursday': thursday,
               'actual_friday': friday,
               'espacios': spaces}
    return render(request, 'espacios.html', context)


@login_required
def landing_search(request, products):
    if not products:
        return landing_articles(request)
    else:
        context = {'productos': products,
                   'colores': {'D': '#009900',
                               'R': '#ffcc00',
                               'P': '#3333cc',
                               'L': '#cc0000'}
                   }
        return render(request, 'articulos.html', context)


@login_required
def search(request):
    if request.method == "GET":
        query = request.GET['query']
        # a_type = "comportamiento_no_definido"
        a_state = "A" if (request.GET['estado'] == "A") else request.GET['estado']

        if not (a_state == "A"):
            articles = Article.objects.filter(state=a_state, name__icontains=query.lower())
        else:
            articles = Article.objects.filter(name__icontains=query.lower())

        products = None if (request.GET['query'] == "") else articles
        return landing_search(request, products)


cache_checked=[]

# Filtra espacios segun opciones de checkbox
def filtro_spaces(request):

    global cache_checked
    if request.method == "POST":
        espacios = request.POST.getlist('checkbox')

        cache_checked=espacios

        return landing_spaces(request, espacios_filtrados=cache_checked)
    else:
        return landing_spaces(request, espacios_filtrados=cache_checked)

def new_reservation(request):
    hini = request.GET.get('hi','')
    if hini.startswith('9:'):
      hini = '0' + hini
    if hini.endswith(':0'):
      hini += '0'
    hfin = request.GET.get('hf','')
    if hfin.endswith(':0'):
      hfin += '0'
    dia = request.GET.get('dt', '')
    dia = datetime.datetime.strptime(dia, '%d/%m/%Y')
    dia = dia.strftime('%Y-%m-%d')
    context = {"h_ini": hini,
               "h_fin": hfin,
               "dia": dia,
               "spaces": Space.objects.all()}
    return render(request, 'nueva_reserva.html', context)

def make_reservation(request):
    if request.method == 'POST':
      r_date = request.POST['fechaReserva']
      hora_ini = request.POST['horaInicio']
      hora_fin = request.POST['horaTermino']
      space = Space.objects.get(id = request.POST['espacio'])
      
      if request.user.enabled:
        string_inicio = r_date + " " + hora_ini
        start_datetime = datetime.datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = r_date + " " + hora_fin
        end_datetime = datetime.datetime.strptime(string_fin, '%Y-%m-%d %H:%M')
        reservation = Reservation(space=space, starting_date_time=start_datetime, ending_date_time=end_datetime, user=request.user)
        reservation.save()
        messages.success(request, 'Pedido realizado con exito')
      else:
        messages.warning(request, 'Usuario no habilitado para pedir prestamos') 
      return HttpResponse("Reserva realizada con exito!")

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from django.db.models.functions import Lower
import datetime
from spacesApp.models import Space
from articlesApp.models import Article
from reservationsApp.models import Reservation
from loansApp.models import Loan
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def landing_articles(request):
    articles = Article.objects.all()
    context = {'productos' : articles}
    return landing_search(request, articles)


def landing_spaces(request, date=None, espacios_filtrados=[]):
    spaces = Space.objects.all().order_by(Lower('name'))
    get_date(request)

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
               'espacios_filtrados': espacios_filtrados,
               'espacios': spaces}
    return render(request, 'espacios.html', context)


@login_required
def landing_search(request, products):
    context = {'productos' : products,
                 'colores' : {'D': '#009900',
                              'R': '#ffcc00',
                              'P': '#3333cc',
                              'L': '#cc0000'}
              }
    return render(request, 'articulos.html', context)

@login_required
def search(request):
    if request.method == "GET":
        nombre = request.GET['nombre']
        articles = Article.objects.filter(name__icontains=nombre.lower())
        prestamos = Loan.objects.filter(article__name__icontains=nombre.lower())

        # ID filtering
        id = request.GET['id']
        if id != "":
            articles = articles.filter(pk=id)                # Filtrar los articulos cuya pk=id
            if articles.exists():
                prestamos = prestamos.filter(article__id=id) # Si existen guardarlos con sus prestamos
            else:
                articles = None
                prestamos = None

        # State filtering
        estado = request.GET['estado']
        if estado != "" and articles != None:
            articles = articles.filter(state=estado)
            if articles.exists():
                for a in articles:
                    auxid = a.id
                    if prestamos.filter(article_id=auxid).exists():
                        prestamos = prestamos.filter(article__id=auxid) # Si existe uno, guardar sus prestamos
            else:
                articles = None
                prestamos = None

        # Time range filtering
        finicial = request.GET['finicial']
        hinicial = request.GET['hinicial']
        ffinal = request.GET['ffinal']
        hfinal = request.GET['hfinal']
        if finicial != "" and ffinal != "" and articles != None:
            cinicial = finicial + " " + hinicial
            cfinal = ffinal + " " + hfinal
            prestamos = prestamos.filter(starting_date_time__gte = cinicial,ending_date_time__lte = cfinal)
            if prestamos.exists():
                for p in prestamos:
                    auxid = p.article.id
                    articles = articles.exclude(pk=auxid)

    return landing_search(request, articles)


cache_checked = []
cache_date = ''


#captura fecha desde la url
def get_date(request):
    global cache_date
    if request.method == "GET":
        date = request.GET.get('date')
        cache_date = date
        return cache_date

# Filtra espacios segun opciones de checkbox
def filtro_spaces(request):
    get_date(request)
    global cache_checked
    if request.method == "POST":
        espacios = request.POST.getlist('checkbox')

        cache_checked = espacios

        return landing_spaces(request, date=cache_date, espacios_filtrados=cache_checked)
    else:
        return landing_spaces(request, date=cache_date, espacios_filtrados=cache_checked)




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
        
        if not 9 <= int(start_datetime.hour) <= 18:
          messages.warning(request, "Error: No se pueden realizar reservas de salas en ese horario")
        elif not 9 <= int(end_datetime.hour) <= 18:
          messages.warning(request, "Error: No se pueden realizar reservas de salas en ese horario")
        elif ((start_datetime - datetime.datetime.now()).seconds / 3600) < 1 and (start_datetime - datetime.datetime.now()).days == 1:
          messages.warning(request, "Error: El quincho debe pedirse con por lo menos un hora de anticipacion")
        else:
          reservation = Reservation(space=space, starting_date_time=start_datetime, ending_date_time=end_datetime, user=request.user)
          reservation.save()
          messages.success(request, 'Pedido realizado con éxito')
      else:
        messages.warning(request, 'Error: Usuario no habilitado para pedir prestamos')
      return HttpResponse("Reserva realizada con exito!")

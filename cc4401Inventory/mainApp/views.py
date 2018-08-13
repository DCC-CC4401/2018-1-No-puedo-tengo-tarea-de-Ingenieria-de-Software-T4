from django.shortcuts import render
from django.utils.timezone import localtime
import datetime
from articlesApp.models import Article
from reservationsApp.models import Reservation
from loansApp.models import Loan
from django.contrib.auth.decorators import login_required


@login_required
def landing_articles(request):
    articles = Article.objects.all()
    context = {'productos' : articles}
    return landing_search(request, articles)


@login_required
def landing_spaces(request, date=None):

    if date:
        current_date = date
        current_week = datetime.datetime.strptime(current_date,"%Y-%m-%d").date().isocalendar()[1]
    else:
        try:
            current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
            current_date = request.GET["date"]
        except:
            current_week = datetime.date.today().isocalendar()[1]
            current_date = datetime.date.today().strftime("%Y-%m-%d")

    reservations = Reservation.objects.filter(starting_date_time__week = current_week, state__in = ['P','A'])
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
        res_list[r.starting_date_time.isocalendar()[2]-1].append(reserv)

    move_controls = list()
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2])-1
    monday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%d/%m/%Y"))
    context = {'reservations' : res_list,
               'current_date' : current_date,
               'controls' : move_controls,
               'actual_monday' : monday}
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

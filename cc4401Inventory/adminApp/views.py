from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reservationsApp.models import Reservation
from loansApp.models import Loan
from articlesApp.models import Article
from spacesApp.models import Space
from mainApp.models import User, Item
from datetime import datetime, timedelta, date
import pytz
from django.utils.timezone import localtime


@login_required
def user_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_panel.html', context)

@login_required
def actions_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    try:
        current_week = datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
        current_date = request.GET["date"]
    except:
        current_date = date.today().strftime("%Y-%m-%d")
        current_week = date.today().isocalendar()[1]

    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)',
               'R': 'rgba(153, 0, 0,0.7)'}

    reservations = Reservation.objects.filter(reservation_state='P').order_by('-action_date_time')
    current_week_reservations = Reservation.objects.filter(starting_date_time__week=current_week)
    actual_date = datetime.now(tz=pytz.utc)
    try:
        if request.method == "GET":
            if request.GET["filter"] == 'perdidos':
                loans = Loan.objects.filter(loan_state='P').order_by('-action_date_time')
            elif request.GET["filter"] == 'caducados':
                loans = Loan.objects.filter(loan_state='C').order_by('-action_date_time')
            elif request.GET["filter"] == 'recibidos':
                loans = Loan.objects.filter(loan_state='R').order_by('-action_date_time')
            elif request.GET["filter"] == 'vigentes':
                loans = Loan.objects.filter(loan_state='V').order_by('-action_date_time')
            else:
                loans = Loan.objects.all().order_by('-action_date_time')
    except:
        loans = Loan.objects.all().order_by('-action_date_time')
    try:
        if request.method == "GET":
            if request.GET["filter"] == 'pendientes':
                reservations = Reservation.objects.filter(reservation_state='P').order_by('-action_date_time')
            elif request.GET["filter"] == 'vigentes':
                reservations = Reservation.objects.filter(reservation_state='V').order_by('-action_date_time')
            elif request.GET["filter"] == 'rechazados':
                reservations = Reservation.objects.filter(reservation_state='R').order_by('-action_date_time')
            else:
                reservations = Reservation.objects.all().order_by('-action_date_time')
    except:
        reservations = Reservation.objects.filter(reservation_state='P').order_by('-action_date_time')

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in current_week_reservations:
        reserv = list()
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores[r.state])
        res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

    move_controls = list()
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
    monday = (
        (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=delta)).strftime("%d/%m/%Y"))

    context = {
        'reservations_query': reservations,
        'loans': loans,
        'reservations': res_list,
        'current_date': current_date,
        'controls': move_controls,
        'actual_monday': monday
    }
    return render(request, 'actions_panel.html', context)


@login_required
def modify_reservations(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":
        accept = True if (request.POST["accept"] == "1") else False
        reservations = Reservation.objects.filter(id__in=request.POST.getlist("selected"))
        if accept:
            for reservation in reservations:
                #space = Space.objects.get(id=reservation.space.id)
                #space.state = 'P'
                #space.save()
                reservation.reservation_state = 'V'
                reservation.save()
        else:
            for reservation in reservations:
                space = Space.objects.get(id=reservation.space.id)
                space.state = 'D'
                space.save()
                reservation.reservation_state = 'R'
                reservation.save()
    return redirect('/admin/actions-panel')


@login_required
def modify_loans(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":
        accept = request.POST["accept"]
        loans = Loan.objects.filter(id__in=request.POST.getlist("selected"))
        if accept == "1":
            for loan in loans:
                article = Article.objects.get(id=loan.article.id)
                article.state = 'D'
                article.save()
                loan.loan_state = 'R'
                loan.save()
        elif accept == "0":
            for loan in loans:
                article = Article.objects.get(id=loan.article.id)
                article.state = 'L'
                article.save()
                loan.loan_state = 'P'
                loan.save()
        elif accept == "2":
            for loan in loans:
                #article = Article.objects.get(id=loan.article.id)
                #article.state = 'P'
                #article.save()
                loan.loan_state = 'V'
                loan.save()
    return redirect('/admin/actions-panel')


@login_required
def items_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    articles = Article.objects.all()
    spaces = Space.objects.all()
    context = {
        'articles': articles,
        'spaces': spaces
    }
    return render(request, 'items_panel.html', context)

from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from spacesApp.models import Space


def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('reservation')
        try:
            for reservation_id in reservation_ids:
                reservation = Reservation.objects.get(pk=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('user_data', user_id=request.user.id)

@login_required
def reservation_data(request, Reservation_id):
    try:
        reservation = Reservation.objects.get(id=Reservation_id)
        space = Space.objects.get(id=reservation.space_id)
        logged_user_id = int(request.session['_auth_user_id'])
        pretty_starting_datetime = reservation.starting_date_time.strftime("%A, %d/%m/%y a las %H:%M")
        pretty_ending_datetime = reservation.starting_date_time.strftime("%A, %d/%m/%y a las %H:%M")

        context = {
            'reservation': reservation,
            'space'      : space,
            'is_requesting_user': reservation.user.id == logged_user_id,
            'pretty_starting_dt': pretty_starting_datetime,
            'pretty_ending_dt': pretty_ending_datetime
        }

        return render(request, 'reservation_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')

@login_required
def delete_reservation(request):
    reservation = Reservation.objects.get(id=request.POST['reservation_id'])
    logged_user_id = int(request.session['_auth_user_id'])

    if (reservation.user.id == logged_user_id):
        try:
            reservation.delete()
            return redirect('/')
        except Exception as ex:
            print(ex)
            return redirect('/')
    else:
        return redirect('/reservation/' + str(reservation.id))

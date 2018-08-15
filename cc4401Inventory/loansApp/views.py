from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from loansApp.models import Loan
from articlesApp.models import Article


# Create your views here.
@login_required
def loan_data(request, loan_id):
    logged_user_id = int(request.session['_auth_user_id'])

    try:
        loan = Loan.objects.get(id=loan_id)
        pretty_starting_datetime = loan.starting_date_time.strftime("%A, %d/%m/%y a las %H:%M")
        pretty_ending_datetime = loan.starting_date_time.strftime("%A, %d/%m/%y a las %H:%M")
        context = {'loan':loan,
                   'pretty_starting_dt': pretty_starting_datetime,
                   'pretty_ending_dt': pretty_ending_datetime,
                   'is_requesting_user': loan.user.id == logged_user_id
                   }
        return render(request, 'loansApp/loan_data.html', context)
    except Exception as ex:
        print('Something happened on loan_data')
        print(ex)
        return redirect('/')

@login_required
def declare_lost_loan(request):
    loan = Loan.objects.get(id=request.POST['loan_id'])
    logged_user_id = int(request.session['_auth_user_id'])

    if (loan.user.id == logged_user_id):
        try:
            loaned_article = Article.objects.get(id=loan.article.id)
            loaned_article.state = 'L'
            loaned_article.save()

            return redirect('/loan/'+str(loan.id))
        except Exception as ex:
            print('Something happened in declare_lost_loan')
            print(ex)
            return redirect('/')
    else:
        return redirect('/loan/' + str(loan.id))
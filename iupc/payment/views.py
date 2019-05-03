from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from payment.models import PaymentStatus


def home(request):
    page_length = 20

    team_list = PaymentStatus.objects.order_by('university', 'team_name')

    # user_list = Profile.objects.order_by('-level_completed')
    paginator = Paginator(team_list, page_length)  # Show 25 contacts per page

    page = request.GET.get('page')
    if page is None:
        page = 1

    users = paginator.get_page(page)

    return render(request, 'payment_front_end/home.html', {'users': users,})
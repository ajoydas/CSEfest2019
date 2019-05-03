from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse

ALUMNI = 0
STUDENT = 1


def validate_user(request, username, email):
    try:
        user = User.objects.get(Q(username=username) | Q(email=email))
    except User.DoesNotExist:
        user = None

    if user is not None:
        # user already exists
        return True
    else:
        return False


# Create your views here.
def register(request):
    # user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if validate_user(request, username, email):
            # user already exists
            msg = "User with this username or email already exists! :("
            messages.add_message(request, messages.ERROR, msg)
            return render(request, 'core_front_end/register.html', {
                'user_state': "exists",
            })
        else:
            # new user
            user = User.objects.create_user(username, email, password)
            user.save()

            login(request, user)
            msg = "Welcome to the contest of the CSE FEST 2019!"
            messages.add_message(request, messages.SUCCESS, msg)
            """
            @send user the first quiz whose pk is 1
            """
            return redirect('quiz:question', 1)

    else:
        return render(request, 'core_front_end/register.html')
        # if user.is_authenticated:
        #     return render(request, 'core_front_end/why_yoy_lyin.html')
        # else:
        #     return render(request, 'core_front_end/register.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('quiz:question', 1)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome back!')
            return redirect('quiz:question', 1)
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')
            return render(request, 'core_front_end/login.html', {
                'view': 'login',
            })
    else:
        return render(request, 'core_front_end/login.html', {
            'view': 'login',
        })


@login_required
def logout_user(request):
    logout(request)
    msg = "Hope to see you soon! :)"
    messages.add_message(request, messages.INFO, msg)
    return redirect('core:login_user')


@login_required
def home(request):
    if request.user.is_authenticated:
        return redirect('quiz:question', 1)

    return  redirect('core:login_user')

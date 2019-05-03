import random
import string

from django.contrib.auth.decorators import login_required, user_passes_test
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


def gen_key():
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return x


@user_passes_test(lambda u: u.is_superuser)
def register(request):
    # user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if validate_user(request, username, None):
            # user already exists
            msg = "User with this username or email already exists! :("
            messages.add_message(request, messages.ERROR, msg)
            return render(request, 'core_front_end/register.html', {
                'user_state': "exists",
            })
        else:
            # new user
            if password is None or password == '':
                password = gen_key()

            user = User.objects.create_user(username,None, password)
            user.save()

            user.profile.start_code = gen_key()
            user.profile.password = password
            user.save()

            msg = "User added successfully"
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect('core:register')

    else:
        return render(request, 'core_front_end/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print(username)
        # print(password)


        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome!')
            return redirect('hunt:hunt')

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


def home(request):
    if not request.user.is_authenticated:
        return redirect('core:login_user')
    return redirect('hunt:hunt')


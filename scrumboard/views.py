from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
from .models import Message


def logoutView(request):
    u = User.objects.get(id=request.user.id)
    u.is_active = False
    u.save()
    logout(request)
    return redirect('login')


def registerView(request):
    form = CreateUserForm()

    if request.method == 'GET':
        if not request.user.is_anonymous:
            return redirect('/scrumboard/')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            new_user = User.objects.get(username=form.cleaned_data['username'])
            new_user.is_active = False

            messages.success(request, 'Account successfully created')
            return redirect('login')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'register.html', context)


def loginView(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            return redirect('/scrumboard/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        u = User.objects.get(username=username)

        if not u.is_active:
            u.is_active = True
            u.save()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/scrumboard/')
        else:
            messages.error(request, 'Username/Password combination is incorrect!')
            return render(request, 'login.html')

    context = {}
    return render(request, 'login.html', context)


def home(request):
    users = User.objects.order_by('-username')[:5]
    context = {'users': users}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def usersView(request):
    users = []
    search = ''
    if request.method == 'GET':
        search = request.GET.get('search')
        if search != '' and search is not None:
            users = User.objects.order_by('-username').filter(username__iregex=search)
        else:
            users = User.objects.order_by('-username')
    context = {'users': users, 'search': search}
    return render(request, 'users.html', context)


@login_required(login_url='login')
def userChat(request, user_id):
    user_to = User.objects.get(id=user_id)

    my_messages = Message.objects.filter(from_user=request.user.id, to_user=user_to.id).values()
    user_messages = Message.objects.filter(from_user=user_to.id, to_user=request.user.id).values()
    all_messages = my_messages | user_messages
    all_messages = all_messages.order_by('date')

    context = {'userTo': user_to, 'messages': all_messages}
    return render(request, 'messages.html', context)


def email(from_user_id, chat, to_user_id):
    from_user = User.objects.get(id=from_user_id)
    to_user = User.objects.get(id=to_user_id)

    subject = 'You have received a message through ChatApp from ' + from_user.username
    message = 'Message: ' + chat + '\n' + 'Login through ChatApp to respond or send an email to: ' + from_user.email
    email_from = settings.EMAIL_HOST_USER

    recipient_list = [to_user.email]
    if not to_user.is_active:
        send_mail(subject, message, email_from, recipient_list)
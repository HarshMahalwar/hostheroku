from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import book, Topic
from .forms import bookForm, TopicForm, participantForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username or password is invalid.')
    context = {'page': page}
    return render(request, 'login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "The user already exists.")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "The password is incorrect.")
            return redirect('register')
    context = {'page': page}
    return render(request, 'register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    t = book.objects.filter(Q(topic__name__icontains=q) |
                              Q(title__icontains=q) |
                              Q(desc__icontains=q)|
                              Q(host__username__icontains=q)|
                            Q(participant__name__icontains=q)
                              )
    room_count = t.count()
    t1 = Topic.objects.all()
    context = {'books': t, 'topic': t1, 'room_count': room_count}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def add(request):
    t = bookForm()
    if request.method == 'POST':
        fr = bookForm(request.POST)
        if fr.is_valid():
            fr.save()
            return redirect('home')
    context = {'books': t}
    return render(request, 'book_form.html', context)


@login_required(login_url='login')
def add_topic(request):
    t1 = TopicForm()

    if request.method == 'POST':
        fr1 = TopicForm(request.POST)
        if fr1.is_valid():
            fr1.save()
            return redirect('home')
    context = {'books': t1}
    return render(request, 'book_form.html', context)


@login_required(login_url='login')
def add_participant(request):
    t1 = participantForm()

    if request.method == 'POST':
        fr1 = participantForm(request.POST)
        if fr1.is_valid():
            fr1.save()
            return redirect('home')
    context = {'books': t1}
    return render(request, 'book_form.html', context)


def deleteBook(request, pk):
    r = book.objects.get(id=pk)
    if request.user != r.host:
        return render(request,"sneaky.html")
    if request.method == 'POST':
        r.delete()
        return redirect('/')
    context = {'book': r}
    return render(request, 'delete.html', context)





def linkedin(request):
    return redirect('https://www.linkedin.com/in/harsh-mahalwar-4310b316a/')


def github(request):
    return redirect('https://github.com/HarshMahalwar?tab=repositories')


def updateBook(request, pk):
    r = book.objects.get(id=pk)
    fr = bookForm(instance=r)
    if request.user != r.host:
        return render(request, "sneaky.html")
    if request.method == 'POST':
        fr = bookForm(request.POST, instance=r)
        if fr.is_valid():
            fr.save()
            return redirect('/')
    context = {'books': fr}
    return render(request, 'update_page.html', context)


def about(request):
    return redirect('https://harshmahalwar.github.io/portfolio/')


# Create your views here.

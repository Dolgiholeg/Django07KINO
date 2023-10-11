from django.shortcuts import render
from .models import*
from django.contrib.auth.models import User, Group

def index(req):
    numkino = Kino.objects.all().count()
    numactor = Actor.objects.all().count()
    numfree = Kino.objects.filter(status__kino=1).count()
    if req.user.username:
        username = req.user.first_name
    else:
        username = 'ГОСТЬ'
    data = {'k1': numkino, 'k2': numactor, 'k3': numfree, 'username': username}
    #user = User.objects.create_user('User2','user2@mail.ru', 'useruser')
    #user.first_name = 'Vlad'
    #user.last_name = 'Petrov'
    #user.save()

    return render(req, 'index.html', context=data)

from django.views import generic
class Kinolist(generic.ListView):
    model = Kino
    paginate_by = 5

class Actorlist(generic.ListView):
    model = Actor
    paginate_by = 5

class Directorlist(generic.ListView):
    model = Director
    paginate_by = 5

class KinoDetail(generic.DetailView):
    model = Kino

class ActorDetail(generic.DetailView):
    model = Actor

class DirectorDetail(generic.DetailView):
    model = Director

from django.http import HttpResponse
def info(req, id):
    film = Kino.objects.get(id=id)
    return HttpResponse(film.title)

def status(req):
    k1 = Status.objects.all()
    data = {'podpiska': k1}
    return render(req, 'podpiska.html', data)

def prosmotr(req, id1, id2, id3):
    status = 0
    print(id1, id2, id3)
    mas = ['бесплатная', 'базовая', 'супер'] #kino id2
    mas2 = ['Free', 'Base', 'Super'] #user id3 status
    if id3 != 0:
        status = User.objects.get(id=id3) #нашли юзера
        status = status.groups.all() #нашли его подписки
        status = status[0].id #нашли айди его подписки(она одна)
        print(status)
    else:
        if id3 == 0: #выдаёт гостю подписку номер1 - бесплатную
            status = 1

    if status >= id2: #сравниваем статус и разрешение на просмотр фильма
        print('OK')
        permission = True
    else:
        print('НЕЛЬЗЯ')
        permission = False

    k1 = Kino.objects.get(id=id1).title
    k2 = Group.objects.get(id=status).name
    k3 = Status.objects.get(id=id2).name
    data = {'kino': k1, 'status': k2, 'statuskino': k3, 'prava': permission}
    return render(req, 'prosmotr.html', data)

def buy(req, type):
    usid = req.user.id #находим номер текущего пользователя
    user123 = User.objects.get(id=usid) #находим его в табличке user
    statusnow = user123.groups.all()[0].id #номер его подписки(группы)
    grold = Group.objects.get(id=statusnow) #находим его подписку в таблице group
    grold.user_set.remove(user123) #удаляем старую подписку
    grnew = Group.objects.get(id=type) #находим новую подписку
    grnew.user_set.add(user123) #добавляем новую подписку
    k1 = grnew.name
    data = {'podpiska': k1}
    return render(req, 'buy.html', data)

from .form import SignUpform
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
def registr(req):
    print(1)
    if req.POST:
        print(2)
        anketa = SignUpform(req.POST)
        if anketa.is_valid():
            print(3)
            anketa.save()
            k1 = anketa.cleaned_data.get('username')
            k2 = anketa.cleaned_data.get('password1')
            k3 = anketa.cleaned_data.get('first_name')
            k4 = anketa.cleaned_data.get('last_name')
            k5 = anketa.cleaned_data.get('email')
            user = authenticate(username=k1, password=k2) #сохраняет нового пользоватлея
            man = User.objects.get(username=k1)             #найдем нового юзера
            #заполним поля в таблице
            man.email=k5
            man.first_name=k3
            man.last_name=k4
            man.save()
            login(req,user) #входит на сайт
            group = Group.objects.get(id=1)#находим бесплатную подписку
            group.user_set.add(man)#записываем юзера в подписку
            return redirect('home')

    else:
        anketa = SignUpform()
    data={'regform':anketa}
    return render(req,'registration/registration.html',context=data)
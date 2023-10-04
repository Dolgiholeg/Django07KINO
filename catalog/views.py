from django.shortcuts import render
from .models import*
from django.contrib.auth.models import User

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
    paginate_by = 2

class KinoDetail(generic.DetailView):
    model = Kino

from django.http import HttpResponse
def info(req,id):
    film = Kino.objects.get(id=id)
    return HttpResponse(film.title)

def status(req):
    k1 = Status.objects.all()
    data = {'podpiska':k1}
    return render(req, 'podpiska.html', data)

def prosmotr(req, id1, id2, id3):
    print(id1, id2, id3)
    mas = ['бесплатная','базовая','супер']#kino id2
    mas2 = ['Free','Base','Super']#user id3 status
    status = User.objects.get(id=id3)#нашли юзера
    status = status.groups.all()#нашли его подписки
    status = status[0].id#нашли айди его подписки(она одна)
    print(status)
    if id3 == 0:#выдаёт гостю подписку номер1 - бесплатную
        status = 1
    if status >= id2:#сравниваем статус и разрешение на просмотр фильма
        print('OK')
    else:
        print('НЕЛЬЗЯ')

    return render(req,'index.html')

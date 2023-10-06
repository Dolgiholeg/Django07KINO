from django.db import models
from django.urls import reverse
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20, verbose_name='Жанр')

    def __str__(self):
        return self.name

class Director(models.Model):
    fname = models.CharField(max_length=20, verbose_name='Имя')
    lname = models.CharField(max_length=20, verbose_name='Фамилия')
    spisok = models.CharField(blank=True, null=True, max_length=100, verbose_name='Фильмы которые снял')

    def __str__(self):
        return f'{self.lname},{self.fname}'
    def get_absolute_url(self):
        return reverse('infodirector', args=[self.id, self.lname])

class Actor(models.Model):
    fname = models.CharField(max_length=20, verbose_name='Имя')
    lname = models.CharField(max_length=20, verbose_name='Фамилия')
    born = models.DateField (blank=True, null=True, verbose_name='Дата рождения')
    country = models.CharField(max_length=20, verbose_name='Страна рождения')
    spisok = models.CharField(blank=True, null=True, max_length=100, verbose_name='Фильмы в которых съиграл')

    def __str__(self):
        return self.lname

    def get_absolute_url(self):
        return reverse('infoactor', args=[self.id, self.lname])

class Status(models.Model):
    VIBOR =(('бесплатно','бесплатно'),('базовая','базовая'),('супер','супер'))
    name = models.CharField(max_length=20, choices=VIBOR, verbose_name='Подписка')

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=20, verbose_name='Страна где снимался фильм')

    def __str__(self):
        return self.name

class AgeRate(models.Model):
    choise = (('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17'))
    rate = models.CharField(max_length=20, choices=choise, verbose_name='Рейтинг')

    def __str__(self):
        return self.rate

class Kino(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    genre = models.ForeignKey(Genre,on_delete=models.SET_DEFAULT, default=1)
    rating = models.FloatField(verbose_name='Оценка')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=500, verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год')
    ager = models.ForeignKey(AgeRate,on_delete=models.SET_NULL, null=True)
    actor = models.ManyToManyField(Actor, verbose_name='Актёры')
    status = models.ForeignKey(Status,on_delete=models.SET_DEFAULT, default=1)
    image = models.CharField(max_length=100, blank=True, null=True, verbose_name='Картинка')

    def __str__(self):
        return self.title

    def display_actors(self):
        res = '  '
        for a in self.actor.all():
            res += a.lname+'  '
        return res
    display_actors.short_description = 'Актёры'

    def get_absolute_url(self):
        return reverse('info', args=[self.id, self.title])
        #return f'kino/{self.id}/{self.title}'




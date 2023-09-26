from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Genre)
#admin.site.register(Director)
#admin.site.register(Actor)
admin.site.register(AgeRate)
#admin.site.register(Status)
#admin.site.register(Kino)
admin.site.register(Country)

class Actoradmin(admin.ModelAdmin):
    list_display = ('fname','lname','born') #столбики в панели админа
    list_display_links = ('fname','lname')  #работают как ссылки
admin.site.register(Actor, Actoradmin)      #регистрация модель актер

class Directoradmin(admin.ModelAdmin):
    list_display = ('fname','lname')
    list_display_links = ('fname','lname')
admin.site.register(Director, Directoradmin)

class Kinoadmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'display_actors')
    list_filter = ('status', 'genre', 'rating')
    fieldsets = (('О фильме',{'fields':('title','summary','actor')}),('Рейтинг',{'fields':('rating','status','ager')})
                 ,('Остальное',{'fields':('country','genre','director','year')})) #набор полей

admin.site.register(Kino, Kinoadmin)

class Stinline(admin.TabularInline):
    model = Kino

class Statusadmin(admin.ModelAdmin):
    inlines = [Stinline]
admin.site.register(Status, Statusadmin)
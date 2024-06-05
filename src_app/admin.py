from django.contrib import admin
from .models import * 


class AudioAdmin(admin.ModelAdmin):

    list_display = ['title']

class ReciterAdmin(admin.ModelAdmin):

    list_display = ['name']


class BookAdmin(admin.ModelAdmin):

    list_display = ['title']

class orderAdmin(admin.ModelAdmin):
    list_display = ['contact', 'book']



admin.site.register(Audio, AudioAdmin)
admin.site.register(Reciter, ReciterAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Order, orderAdmin)



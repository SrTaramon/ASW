from django.contrib import admin
from django.contrib.auth.models import User
from .models import Submit, Comment, Usuari

admin.site.register(Submit)
admin.site.register(Comment)
admin.site.register(Usuari)

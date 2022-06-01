from django.contrib import admin
from .models import *
# Register your models here.

def register(model):

    class AdminModel(admin.ModelAdmin):
        pass
    admin.site.register(model, AdminModel)


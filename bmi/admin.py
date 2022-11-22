from django.contrib import admin
from .models import Bmi

class BmiAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'bmi', 'date')

admin.site.register(Bmi, BmiAdmin)
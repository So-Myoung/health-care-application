from django.urls import path
from django.urls import path, include
from blog import views
from .views import *

urlpatterns = [
    path('', bmi, name='bmi' ),
    # path('', include("bmi.urls"))
]
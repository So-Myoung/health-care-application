from django.urls import path
from django.urls import path, include
from bmi import views
from .views import *

urlpatterns = [
    path('', bmi, name='bmi'),
    path('bmi2',views.bmi2,name='bim2'),
    # path('', include("bmi.urls"))
]
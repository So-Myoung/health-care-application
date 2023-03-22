from django.urls import path

import myapp
from .views import *

urlpatterns = [
    path('', index, name='index'),
]
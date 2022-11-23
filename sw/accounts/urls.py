from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('home/', home, name='home'),
    path('maker/',maker,name='maker'),
    path('bmi/',bmi,name='bmi'),
    path('tab/',tab,name='tab'),
]
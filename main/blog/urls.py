from django.urls import path

from blog import views
from .views import *

urlpatterns = [
    path('', home, name='home' ),
    path('/', board, name='board'),
    path('edit/<int:pk>', boardEdit, name='edit'),
    path('delete/<int:pk>', boardDelete, name='delete'),

]
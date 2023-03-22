from django.urls import path
from .views import *

urlpatterns = [
    path('crawl/', crawl, name='crawl'),
]
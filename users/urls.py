from django.urls import include, path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<slug:uid64>/<slug:token>', activate, name='activate'),
]

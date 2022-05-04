from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
from .forms import *

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<slug:uid64>/<slug:token>', activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/users/login/'), name='logout')
]

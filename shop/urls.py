from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<slug:slug>', views.item_detail, name='item_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]

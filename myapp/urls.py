from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.inicio, name='inicio'), 
    path('cardapio', views.cardapio, name='cardapio'), 
]
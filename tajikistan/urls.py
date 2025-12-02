from django.urls import path, include
from .views import add_bus

urlpatterns = [
    path('add_bus/', add_bus, name = 'add_bus'),
    
]
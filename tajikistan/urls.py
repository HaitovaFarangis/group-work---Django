from django.urls import path, include
from .views import *

urlpatterns = [
    path('bus_create/',bus_create_view, name = 'bus_create'),
    path('add_participant_me/<int:pk>',participant_create_ME_view, name = 'participant_create_me'),
    path('add_participant/<int:pk>',participant_create_view, name = 'participant_create'),
    path('remove_participant',participant_delete_view, name = 'participant_delete'),
    path('landmark_detail/<int:pk>',landmark_detail_view, name = 'landmark_detail'),
    path('',home_list_view, name = 'home_list'),
    
]
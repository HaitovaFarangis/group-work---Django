from django.urls import path
from .views import register_view,verify_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('verify/<int:user_id>/', verify_view, name='verify'),
]

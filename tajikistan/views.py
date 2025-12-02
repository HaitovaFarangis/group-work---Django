from django.shortcuts import render, redirect, HttpResponse
from .models import *


def bus_create_view(request):
    if request.user.is_staff:
        if request.method =="GET":
            return render(request, 'add_bus.html')
        elif request.method == 'POST':
            name = request.POST.get('name', None)
            landmarks = request.POST.get('landmarks', None)
            schedule = request.POST.get('schedule', None)
            
            new_bus = Bus(name = name, landmarks = landmarks, schedule=schedule)
            new_bus.save()
            return HttpResponse('Done')
    else:
        return HttpResponse('You are not admin ')
    
 

# def home_list(request):
#      return render(request, 'home.html')
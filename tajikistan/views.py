from django.shortcuts import render, redirect, HttpResponse
from .models import *


def bus_create_view(request):
    if request.user.is_staff:
        if request.method =="GET":
            landmarks = Landmark.objects.all()
            return render(request, 'add_bus.html', context={'landmarks':landmarks})
        elif request.method == 'POST':
            name = request.POST.get('name', None)
            landmarks = request.POST.get('landmarks', None)
            schedule = request.POST.get('schedule', None)
            
            new_bus = Bus.objects.create(name = name, schedule=schedule)
            new_bus.landmarks.set(landmarks)
            return HttpResponse('Done')
    else:
        return HttpResponse('You are not admin ')


def participant_delete_view(request, pk):
    bus = Bus.objects.filter(id = pk).first()
    if request.user.is_authenticated:
        participants = Participant.objects.filter(user = request.user, bus = bus).first()
        participants.delete()
        return redirect('/')
    else:
        return HttpResponse("login")

 
def participant_create_ME_view(request, pk):
    bus = Bus.objects.filter(id = pk).first()
    if request.user.is_authenticated:
        participants = Participant(user = request.user, bus = bus)
        participants.save()
        return redirect('/')
    else:
        return HttpResponse("login")
        

def participant_create_view(request, pk):
    bus = Bus.objects.get(id=pk)
    if request.method =="GET":
        return render(request, 'participant_create_view.html',context={'bus':bus} )
    if request.method =="POST":
        email = request.POST.get('email', None)
        is_email= CustomUser.objects.filter(email = email).first()
        if is_email:
            participants = Participant(user = is_email, bus = bus)
            participants.save()
            return redirect('/')
        elif not is_email:
            return render(request, 'participant_create_view.html',context={'error':"No such email, try again", 'bus':bus})
from django.shortcuts import render
from .models import Landmark, Participant, Bus

def home_list_view(request):
    if request.user.is_authenticated:
        user_buses = Bus.objects.filter(participants__user=request.user).distinct()

        landmarks = Landmark.objects.filter(buses__in=user_buses).distinct()
    else:
        landmarks = Landmark.objects.none()

    return render(request, 'home_page.html', context={'landmarks': landmarks})


def landmark_detail_view(request, pk):
    landmark = Landmark.objects.filter(id=pk).first()
    buses_data = []

    if landmark:
        buses = landmark.buses.all()

        for bus in buses:
            if request.user.is_authenticated:
                is_participant = Participant.objects.filter(user=request.user, bus=bus).exists()
            else:
                is_participant = False
            buses_data.append({
                "bus": bus,
                "participants": bus.participants.all(),
                "participants_count": bus.participants.count(),
                "is_participant": is_participant
            })

    context = {
        "landmark": landmark,
        "buses_data": buses_data,
    }
    return render(request, 'landmark_detail.html', context)

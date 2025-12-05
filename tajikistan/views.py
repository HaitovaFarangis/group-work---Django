
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .models import *

def bus_create_view(request):
    if request.user.is_staff:
        if request.method =="GET":
            landmarks = Landmark.objects.all()
            return render(request, 'add_bus.html', context={'landmarks':landmarks})
        elif request.method == 'POST':
            name = request.POST.get('name', None)           
            schedule = request.POST.get('schedule', '')
            landmarks_raw = request.POST.get("landmarks", "")
            landmarks_ids =[
                int(x.strip()) for x in landmarks_raw.split(',') if x.strip().isdigit()
            ]
            
            new_bus = Bus.objects.create(name = name, schedule=schedule)
            new_bus.landmarks.set(landmarks_ids)
            return redirect('/')
    else:
        return HttpResponse('You are not admin ')


def participant_delete_view(request, pk):
    bus = get_object_or_404(Bus, id=pk) 
    if request.user.is_authenticated:
        participant = Participant.objects.filter(user=request.user, bus=bus).first()
        if participant:
            participant.delete()
        return redirect('home_list')
    else:
        return redirect('login')


 
def participant_create_ME_view(request, pk):
    bus = Bus.objects.filter(id = pk).first()
    if request.user.is_authenticated:
        participants = Participant(user = request.user, bus = bus)
        participants.save()
        return redirect('/')
    else:
        return redirect("login")
        

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
            return render(request, 'participant_create_view.html',context={'error':"No such email, try again. Only those who registered can be added to tournament ", 'bus':bus})
        
        
def home_list_view(request):
    all_landmarks = Landmark.objects.all()

    user_buses = None
    if request.user.is_authenticated:
        user_buses = Bus.objects.filter(participants__user=request.user).distinct()

    context = {
        'landmarks': all_landmarks,
        'user_buses': user_buses,
    }

    return render(request, 'home_page.html', context)

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

def landmarks_list_view(request):
    landmarks_list = Landmark.objects.all()
    return render(request, 'landmarks.html',context={'landmarks':landmarks_list})
# def home(request):
#     return render(request, 'home.html')

def my_profile(request):
    return render(request, 'my_profile.html')

def my_bookings(request):
    return render(request, 'my_bookings.html')
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

def home(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=search) |
        Q(name__icontains=search) |
        Q(description__icontains=search) |
        Q(host__username__icontains=search)
        )
    room_count = rooms.count()

    topics = Topic.objects.all()

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}

    return render(request, 'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj':room}
    return render(request, 'base/delete.html', context)
    
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)

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
    activities = Message.objects.filter(Q(room__topic__name__icontains=search)).order_by('-created')

    context = {'rooms':rooms, 'topics':topics, 
               'room_count':room_count, 'activities':activities}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room).order_by('created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id) # type: ignore

    context = {'room':room, 'room_messages':messages, 'participants':participants}
    return render(request, 'base/room.html',context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(host=user) 
    activities = Message.objects.filter(user=user)
    topics = Topic.objects.all()

    context = {'user':user, 'rooms':rooms,
               'activities':activities, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj':room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='/login')
def deleteMessage(request, pk, roomId):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=roomId)
    
    context = {'obj':message}
    return render(request, 'base/delete.html', context)

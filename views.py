
from django.shortcuts import render, redirect
from .models import Message, Room, Topic
from .forms import RoomForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower

        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "USER not exist")    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
             

        else:
            return redirect('home')
           

            print(user)     

        
    context = {}
    return render(request, 'base/login_reg.html', context)

def signup(request):
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
            messages.error(request, "please sign up")


            return render(request, 'base/signup.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)


    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    #participant = Room.objects.all()
    if request.method == 'POST':
        message = Message.objects.create(
            
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk=room.id)


    context = {'room':room, 'room_messages':room_messages}

    return render(request, 'base/room.html', context)




def profile(request):
    #user = User.objects.get(id=pk)
    #rooms = user.room_set.all()

    #context = {'user':user, 'rooms':rooms}
    return render(request, 'base/profile.html')


# Create your views here.
def create(request):
    form = RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)



def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def deleterooom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
   



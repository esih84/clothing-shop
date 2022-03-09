from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .models import Chat,Message
from django.views.generic.edit import UpdateView ,DeleteView

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    chat_rooms = Chat.objects.filter(members=user)
    context = {
        'chat_rooms': chat_rooms
    }
    return render(request,"chat/index.html",context)


@login_required(login_url='/accounts/login/')
def room(request, room_name):
    user = request.user
    chat_model = Chat.objects.filter(roomname=room_name)
    if not chat_model.exists():
        chat = Chat.objects.create(roomname=room_name)
        chat.members.add(user)
    else:
        chat_model[0].members.add(user)

    username = request.user.username
    context = {
        'room_name': room_name,
        'username': mark_safe(json.dumps(username)),
    }
    return render(request, "chat/room.html", context)

class edit_chat(UpdateView):
    model = Message
    template_name = "chat/edit_chat.html"
    fields = ['content']

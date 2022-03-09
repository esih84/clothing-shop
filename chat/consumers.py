from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from .models import Message,Chat
from rest_framework.renderers import JSONRenderer
from accounts.models import User

class ChatConsumer(WebsocketConsumer):


    def new_message(self,data):
        message = data['message']
        author = data['username']
        roomname = data['roomname']
        chat_model = Chat.objects.get(roomname=roomname)
        user_model = User.objects.filter(username=author).first()
        message_model=Message.objects.create(author=user_model ,content=message,related_chat=chat_model)
        result =self.message_serializer(message_model)
        result=eval(result)['content']
        self.send_to_chat_message(result)


    def fetch_message(self,data):
        roomname= data['roomname']
        qs=Message.last_message(self,roomname)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
            'command':"fetch_message"
        }
        self.chat_message(content)




    def message_serializer(self,qs):



        serialized = MessageSerializer(qs,many=(lambda qs : True if(qs.__class__.__name__== 'QuerySet')else False)(qs))
        content = JSONRenderer().render(serialized.data)
        return content
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()

    commands ={
        "new_message":new_message,
        "fetch_message":fetch_message,
    }

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self,text_data):
        text_data_dict = json.loads(text_data)
        # daryaft payam az samte karbar

        command = text_data_dict['command']

        self.commands[command](self,text_data_dict)

    def send_to_chat_message(self,message):
        async_to_sync(self.channel_layer.group_send)(

            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'command':'new_message',
            }
        )

    def chat_message(self, event):
        # event as send_to_chat_message group_send omade
        self.send(text_data=json.dumps(event))
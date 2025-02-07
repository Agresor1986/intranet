import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName, 
            self.channel_name 
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        timestamp = datetime.now().timestamp()  

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "timestamp": timestamp
            }
        )
    
    async def sendMessage(self, event): 
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timestamp
        }))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.room_name = f"private_{min(self.scope['user'].username, self.other_username)}_{max(self.scope['user'].username, self.other_username)}"
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username
        timestamp = datetime.now().timestamp()

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': timestamp,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))

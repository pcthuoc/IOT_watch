# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from sensors.models import Sensors

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"sensor_user_{self.user.id}"  # Đổi tên group khớp với group_send
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # Nếu frontend gửi gì đó

    # 👇 Đây là hàm xử lý khi backend gọi group_send với type = "send_sensor_data"
    async def send_sensor_data(self, event):
        await self.send(text_data=json.dumps({
            "sensor_id": event["sensor_id"],
            "value": event["value"],
            "updated_at": event["updated_at"]
        }))
class TTSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"tts_user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"[WS] {self.user.username} đã kết nối tới nhóm {self.group_name}")
        else:
            print("[WS] Người dùng chưa đăng nhập – đóng kết nối")
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # Không xử lý gì nếu frontend gửi lên

    # Hàm nhận dữ liệu từ backend group_send
    async def tts_played(self, event):
        await self.send(text_data=json.dumps({
            "url": event["url"],
            "status": "played",
            "username": event["username"]
        }))

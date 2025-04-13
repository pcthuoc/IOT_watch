from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensor/$', consumers.SensorConsumer.as_asgi()),
    re_path(r"ws/tts/$", consumers.TTSConsumer.as_asgi()),  # ← dòng này đúng rồi
]

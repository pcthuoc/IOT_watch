# utils.py (hoặc views.py, tùy bạn tổ chức)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_sensor_update(user_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}_sensor",
        {
            "type": "send_sensor_update",
            "data": data,
        },
    )

def notify_tts_played(user_id, message_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}_tts",
        {
            "type": "send_tts_status",
            "data": {
                "status": "played",
                "message_id": message_id,
            },
        },
    )

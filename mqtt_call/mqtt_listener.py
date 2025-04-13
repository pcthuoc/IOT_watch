import paho.mqtt.client as mqtt
import threading
import queue
import json
from django.utils import timezone
from sensors.models import Sensors, SensorData
from alert.models import Alert
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth.models import User


# Hàng đợi xử lý tin nhắn MQTT
mqtt_message_queue = queue.Queue()

# ==== 1. Hàm xử lý kết nối MQTT thành công ====
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully.")
        client.subscribe("IOT/#")  # Sub tất cả topic IOT
    else:
        print(f"[MQTT] Connection failed with code {rc}")

# ==== 2. Hàm nhận tin nhắn MQTT ====
def on_message(client, userdata, msg):
    try:
        mqtt_message_queue.put(msg)
        print(f"[MQTT] Message received from topic: {msg.topic}")
    except Exception as e:
        print(f"[ERROR] Failed to enqueue MQTT message: {e}")

# ==== 3. Hàm xử lý logic từ các topic MQTT ====
def process_mqtt_queue():
    while True:
        try:
            msg = mqtt_message_queue.get()
            topic_parts = msg.topic.split('/')
            payload = msg.payload.decode("utf-8")

            if topic_parts[0] != "IOT":
                continue

            if len(topic_parts) == 2 and topic_parts[1] == "alret":
                handle_alert(payload)
            elif len(topic_parts) == 3 and topic_parts[1] == "sensor":
                sensor_id = topic_parts[2]
                handle_sensor_data(sensor_id, payload)
            elif len(topic_parts) == 3 and topic_parts[1] == "reminder" and topic_parts[2] == "play":
                handle_reminder_play(payload)
            else:
                print(f"[WARNING] Unknown topic structure: {msg.topic}")

            mqtt_message_queue.task_done()
        except Exception as e:
            print(f"[ERROR] Error processing MQTT message: {e}")

# ==== 4. Hàm xử lý dữ liệu cảm biến ====
def handle_sensor_data(sensor_id, payload):
    try:
        # Parse dữ liệu từ MQTT
        try:
            data = json.loads(payload)
            value = float(data.get("value"))
            username = data.get("username")
        except Exception:
            print(f"[ERROR] Invalid payload format: {payload}")
            return

        if not username:
            print(f"[ERROR] Payload thiếu username: {payload}")
            return

        # Tìm user theo username
        user = User.objects.filter(username=username).first()
        if not user:
            print(f"[ERROR] User '{username}' không tồn tại.")
            return

        # Tìm sensor theo sensor_id và user
        sensor = Sensors.objects.filter(sensor_id=sensor_id, user=user).first()
        if not sensor:
            print(f"[INFO] Sensor '{sensor_id}' không thuộc user '{username}'.")
            return

        now = timezone.now()

        # Kiểm tra thời gian ghi trước đó để lưu lịch sử
        last_data = SensorData.objects.filter(sensor=sensor).order_by('-timestamp').first()
        if not last_data or (now - last_data.timestamp).total_seconds() > settings.TIME_SAVE * 60:
            SensorData.objects.create(
                sensor=sensor,
                value=value,
                unit=sensor.unit or ""
            )

        # Cập nhật giá trị và thời gian mới
        sensor.value = value
        sensor.updated_at = now
        sensor.save()

        # Gửi WebSocket tới đúng user
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"sensor_user_{user.id}",
            {
                "type": "send_sensor_data",
                "sensor_id": sensor_id,
                "value": value,
                "updated_at": now.isoformat()
            }
        )

        print(f"[MQTT] Cập nhật thành công sensor '{sensor_id}' cho user '{username}'")

    except Exception as e:
        print(f"[ERROR] handle_sensor_data: {e}")
# ==== 5. Hàm xử lý cảnh báo ====
def handle_alert(payload):
    try:
        data = json.loads(payload)
        message = data.get("message")
        level = data.get("level", "Low").capitalize()
        username = data.get("username")

        if not message or not level or not username:
            print("[WARNING] Thiếu thông tin 'message', 'level', hoặc 'username'")
            return

        # Lấy user từ username
        user = User.objects.filter(username=username).first()
        if not user:
            print(f"[ERROR] User '{username}' không tồn tại.")
            return

        # Tạo bản ghi cảnh báo
        Alert.objects.create(
            user=user,
            message=message,
            level=level
        )
        print(f"[ALERT] {level.upper()} - {message} (User: {username})")

    except Exception as e:
        print(f"[ERROR] Lỗi khi xử lý alert: {e}")
# ==== 6. Hàm xử lý phát reminder ====
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
import json

def handle_reminder_play(payload):
    try:
        data = json.loads(payload)
        url = data.get("url")
        status = data.get("status")
        username = data.get("username")

        if not url or not status or not username:
            print(f"[WARNING] ❗ Thiếu url/status/username trong payload: {data}")
            return

        user = User.objects.filter(username=username).first()
        if not user:
            print(f"[WARNING] ❗ Không tìm thấy user: '{username}'")
            return

        group_name = f"tts_user_{user.id}"
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "tts_played",  # ← trùng với tên method trong TTSConsumer
                "status": status,
            }
        )

        print(f"[TTS ✅] Đã gửi trạng thái '{status}' tới nhóm '{group_name}' | URL: {url}")

    except Exception as e:
        print(f"[ERROR] ❌ Lỗi khi xử lý reminder play payload: {e}")


# ==== 7. Hàm khởi động client MQTT ====
def start_mqtt_listener():
    client = mqtt.Client()
    client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
        client.loop_start()

        processing_thread = threading.Thread(target=process_mqtt_queue)
        processing_thread.daemon = True
        processing_thread.start()

        print("[MQTT] Listener started.")
    except Exception as e:
        print(f"[ERROR] Failed to start MQTT client: {e}")
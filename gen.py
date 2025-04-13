import csv
from datetime import datetime, timedelta
import random

def generate_normal_value(sensor_type):
    if sensor_type == 'temp':
        return round(random.uniform(36.0, 37.5), 1)  # Nhiệt độ bình thường
    elif sensor_type == 'spo2':
        return round(random.uniform(95, 100), 1)     # SPO2 bình thường
    elif sensor_type == 'heart':
        return round(random.uniform(60, 100), 1)     # Nhịp tim bình thường

def generate_sensor_data():
    # Thông tin cảm biến
    sensors = [
        {'id': 'sensor_temp', 'name': 'Nhiệt Độ', 'unit': '°C'},
        {'id': 'sensor_spo2', 'name': 'SPO2', 'unit': '%'},
        {'id': 'sensor_heart', 'name': 'Nhịp Tim', 'unit': 'BPM'}
    ]

    # Thời gian kết thúc và bắt đầu
    end_time = datetime(2025, 4, 14, 1, 22, 0)
    start_time = end_time - timedelta(days=7)
    
    # Tạo file CSV
    with open('sensor_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'sensor__sensor_id', 'sensor__sensor_name', 'value', 'unit', 'timestamp'])
        
        current_id = 1
        current_time = start_time
        
        while current_time <= end_time:
            for sensor in sensors:
                value = generate_normal_value(sensor['id'].split('_')[1])
                writer.writerow([
                    current_id,
                    sensor['id'],
                    sensor['name'],
                    value,
                    sensor['unit'],
                    current_time.strftime('%Y-%m-%d %H:%M:%S')
                ])
                current_id += 1
            current_time += timedelta(minutes=5)

if __name__ == '__main__':
    generate_sensor_data()
    print("Đã tạo xong file sensor_data.csv")
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Sensors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết cảm biến với người dùng
    updated_at = models.DateTimeField(default=timezone.now)  # Thời gian cập nhật, sử dụng giờ của Django
    sensor_id = models.CharField(max_length=255, unique=True)  # Định danh cảm biến (ID cảm biến)
    sensor_name = models.CharField(max_length=255)  # Tên cảm biến (ví dụ: Temperature, pH, etc.)
    value = models.FloatField(null=True, blank=True)  # Giá trị từ cảm biến, có thể để trống
    unit = models.CharField(max_length=50, null=True, blank=True)  # Đơn vị đo, có thể để trống

    def save(self, *args, **kwargs):
        # Kiểm tra nếu sensor_id đã tồn tại, chỉ cập nhật nếu tồn tại
        if self.pk is None:  # Nếu là bản ghi mới, không cần kiểm tra
            existing_sensor = Sensors.objects.filter(sensor_id=self.sensor_id).first()
            if existing_sensor:
                # Nếu cảm biến đã tồn tại, chỉ cập nhật giá trị mà không tạo mới
                self.pk = existing_sensor.pk  # Đặt khóa chính để cập nhật
                self.updated_at = timezone.now()  # Cập nhật thời gian
        super(Sensors, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.sensor_name} ({self.sensor_id}) - {self.value} {self.unit} at {self.updated_at}"

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"
class SensorData(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE, related_name='data_logs', verbose_name="Cảm biến")  # Liên kết với cảm biến
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Thời gian ghi nhận")  # Thời gian ghi nhận dữ liệu
    value = models.FloatField(verbose_name="Giá trị")  # Giá trị đo được
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name="Đơn vị")  # Đơn vị đo

    def __str__(self):
        return f"{self.sensor.sensor_name} - {self.value} {self.unit} @ {self.timestamp}"

    class Meta:
        verbose_name = "Dữ liệu cảm biến"
        verbose_name_plural = "Lịch sử cảm biến"
        ordering = ['-timestamp']

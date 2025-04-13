from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Alert(models.Model):
    LEVEL_LOW = 'Low'
    LEVEL_MEDIUM = 'Medium'
    LEVEL_HIGH = 'High'
    LEVEL_CRITICAL = 'Critical'

    LEVEL_CHOICES = [
        (LEVEL_LOW, 'Thấp'),
        (LEVEL_MEDIUM, 'Trung bình'),
        (LEVEL_HIGH, 'Cao'),
        (LEVEL_CRITICAL, 'Nguy cấp'),
    ]

    # Liên kết với người dùng
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Mỗi cảnh báo thuộc về một người dùng
    
    # Cấp độ cảnh báo
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        default=LEVEL_LOW
    )
    
    # Nội dung cảnh báo
    message = models.TextField()
    
    # Ngày giờ xảy ra cảnh báo
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Alert {self.get_level_display()} - {self.message[:50]}"

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

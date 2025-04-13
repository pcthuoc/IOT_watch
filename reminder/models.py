from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Reminder(models.Model):
    # Liên kết với người dùng
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lời nhắc thuộc về người dùng
    
    # Nội dung lời nhắc
    message = models.TextField()  # Nội dung của lời nhắc
    
    # Thời gian lời nhắc
    remind_at = models.DateTimeField(default=timezone.now)  # Thời gian lời nhắc, mặc định là thời gian hiện tại
    
    # URL liên kết
    url = models.URLField(max_length=200, null=True, blank=True)  # Trường URL có thể để trống
    
    # Trạng thái lời nhắc
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    IGNORED = 'Ignored'

    STATUS_CHOICES = [
        (PENDING, 'Chưa hoàn thành'),
        (COMPLETED, 'Đã hoàn thành'),
        (IGNORED, 'Đã bỏ qua'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
        return f"Reminder for {self.user.username} at {self.remind_at}: {self.message[:50]} - Status: {self.get_status_display()}"

    class Meta:
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"

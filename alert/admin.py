from django.contrib import admin
from .models import Alert

class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'message', 'created_at')
    list_filter = ('level', 'user')  # Lọc theo cấp độ và người dùng
    search_fields = ('message', 'user__username')  # Tìm kiếm theo nội dung cảnh báo và tên người dùng

admin.site.register(Alert, AlertAdmin)

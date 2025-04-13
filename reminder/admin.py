from django.contrib import admin
from .models import Reminder

class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'remind_at', 'status', 'url')
    list_filter = ('status', 'user', 'remind_at')  # Lọc theo trạng thái, người dùng và thời gian
    search_fields = ('message', 'user__username')  # Tìm kiếm theo nội dung lời nhắc và tên người dùng

admin.site.register(Reminder, ReminderAdmin)

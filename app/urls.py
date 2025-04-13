# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app.views import ReminderListView,ReminderAddEditView,AlertListView

urlpatterns = [

    # The home page
    path('', views.dashboard, name='home'),
    path('chart-data/', views.sensor_chart_data, name='sensor_chart_data'),

    path('reminder', ReminderListView.as_view(), name='list_reminder'),  # Danh sách lời nhắc
    path('reminder/add/', ReminderAddEditView.as_view(), name='add_reminder'),  # Thêm lời nhắc
    path('reminder/edit/<int:reminder_id>/', ReminderAddEditView.as_view(), name='edit_reminder'),  # Sửa lời nhắc
    path('reminder/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    
    path('alert', AlertListView.as_view(), name='alert_reminder'),  # Danh sách lời nhắc
    path('alert/delete/<int:alert_id>/', views.delete_alert, name='delete_alert'),

    path('tts/zalo/', views.zalo_tts, name='zalo_tts'),


    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),

]

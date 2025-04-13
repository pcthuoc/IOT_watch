# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.core.paginator import Paginator
from django.shortcuts import render
from reminder.models import Reminder
from alert.models import Alert
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from .forms import ReminderForm
from django.http import JsonResponse, Http404
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone
from sensors.models import Sensors,SensorData
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.conf import settings
import requests
@login_required(login_url="/login/")

def dashboard(request):
    sensors = Sensors.objects.all()
    recent_alerts = Alert.objects.order_by('-created_at')[:5]  # Lấy 5 cảnh báo mới nhất

    context = {
        'segment': 'dashboard',
        'sensors': sensors,
        'recent_alerts': recent_alerts,
    }

    return render(request, 'dashboard.html', context)
def sensor_chart_data(request):
    time_range = request.GET.get('range', '24h')

    time_map = {
        '1h': timedelta(hours=1),
        '3h': timedelta(hours=3),
        '6h': timedelta(hours=6),
        '12h': timedelta(hours=12),
        '24h': timedelta(hours=24),
        '3d': timedelta(days=3),
        '7d': timedelta(days=7),
    }

    duration = time_map.get(time_range, timedelta(hours=24))
    time_threshold = now() - duration

    data = {}
    sensors = Sensors.objects.all()

    for sensor in sensors:
        logs = SensorData.objects.filter(sensor=sensor, timestamp__gte=time_threshold).order_by('timestamp')
        data[sensor.sensor_name] = [
            {
                'x': log.timestamp.isoformat(),  # ApexCharts cần ISO format
                'y': log.value
            } for log in logs
        ]

    return JsonResponse(data)

class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    paginate_by = 5  # Hiển thị 10 file mỗi trang
    template_name = 'reminder_list.html'
    context_object_name = 'reminders'
    login_url = "/login/"

    def get_queryset(self):
        queryset = Reminder.objects.all().order_by('-remind_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'list_reminder'  
        return context
class ReminderAddEditView(View):
    def post(self, request, reminder_id=None):
        if reminder_id:
            reminder = get_object_or_404(Reminder, pk=reminder_id, user=request.user)
        else:
            reminder = None

        form = ReminderForm(request.POST, instance=reminder)
        
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user  # Gán người dùng
            reminder.save()
            return JsonResponse({
                'success': True,
                'message': 'Lời nhắc đã được thêm hoặc sửa thành công!',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Dữ liệu không hợp lệ!',
            })

def delete_reminder(request, reminder_id):
    # Lấy đối tượng Reminder cần xóa (chỉ xóa nếu thuộc về người dùng hiện tại)
    reminder = get_object_or_404(Reminder, pk=reminder_id, user=request.user)

    # Xóa đối tượng
    reminder.delete()

    # Trả về phản hồi JSON
    return JsonResponse({
        'success': True,
        'message': 'Lời nhắc đã được xóa thành công!'
    })

def add_edit_reminder(request, reminder_id=None):
    # Nếu là chỉnh sửa, lấy đối tượng cần sửa
    if reminder_id:
        reminder = get_object_or_404(Reminder, pk=reminder_id, user=request.user)
    else:
        reminder = None  # Nếu là thêm mới, không có đối tượng

    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user  # Gắn người dùng hiện tại
            reminder.save()
            return redirect('reminder_list')  # Chuyển đến trang danh sách lời nhắc
    else:
        form = ReminderForm(instance=reminder)

    return render(request, 'reminder/reminder_form.html', {'form': form, 'reminder': reminder})


class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    paginate_by = 5  # Hiển thị 10 file mỗi trang
    template_name = 'alert_list.html'
    context_object_name = 'alerts'
    login_url = "/login/"

    def get_queryset(self):
        queryset = Alert.objects.all().order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'list_alert'  
        return context

def delete_alert(request, alert_id):
    alert = get_object_or_404(Alert, pk=alert_id, user=request.user)

    # Xóa đối tượng
    alert.delete()

    # Trả về phản hồi JSON
    return JsonResponse({
        'success': True,
        'message': 'Lời nhắc đã được xóa thành công!'
    })


@login_required(login_url="/login/")
def zalo_tts(request):
    if request.method == "GET":
        input_text = request.GET.get("message")
        if not input_text:
            return JsonResponse({"error": "Missing input text"}, status=400)

        payload = {
            "input": input_text,
            "speaker_id": request.GET.get("speaker_id", 1),
            "speed": request.GET.get("speed", 1.0),
            "encode_type": request.GET.get("encode_type", 1),
        }

        headers = {
            "apikey": settings.ZALO_TTS_API_KEY
        }

        try:
            response = requests.post("https://api.zalo.ai/v1/tts/synthesize", data=payload, headers=headers)
            result = response.json()

            if result.get("error_code") == 0:
                audio_url = result["data"]["url"]
                print("🔊 Zalo TTS Audio URL:", audio_url)
                return JsonResponse({"audio_url": audio_url})
            else:
                return JsonResponse({"error": result.get("error_message")}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only GET method is allowed"}, status=405)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

from django import forms
from reminder.models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['message', 'remind_at', 'url', 'status']  # Các trường trong Reminder

import datetime
from datetime import datetime, date, timedelta
import requests
from celery import shared_task
from django.core.management import settings
from habits.models import Habit


@shared_task
def send_message_about_habits():
    time_now = datetime.now().time().replace(second=0, microsecond=0)
    date_now = date.today()
    habits = Habit.objects.all()

    for habit in habits:

        if habit.date is None:
            habit.date = date_now
        if habit.date == date_now:
            if habit.time == time_now:
                if habit.owner.telegram_id:
                    URL = 'https://api.telegram.org/bot'
                    TOKEN = settings.TELEGRAM_TOKEN
                    message = f'Тебе надо выполнить: {habit.action}, текущее время {time_now}'
                    requests.post(
                        url=f'{URL}{TOKEN}/sendMessage',
                        data={
                            'chat_id': habit.owner.telegram_id,
                            'text': message,
                        }
                    )
                    habit.date = date_now + timedelta(days=habit.periodicity)
                    habit.save()

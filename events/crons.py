from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Event
from django_apscheduler.jobstores import DjangoJobStore
from  .utils import send_to_rabbitmq
import json
def notify_worker():
    print("Notifying about events")
    now = timezone.localtime(timezone.now())
    threshold = now + timedelta(minutes=30)
    print(f"Threshold time: {threshold}")
    events = Event.objects.filter(start_time__range=[threshold, threshold+timedelta(minutes=1)])
    if not events:
        print("No events found")

    else:
        print(f"Events: {events}")
        for event in events:
            message = json.dumps({
                "event_id": event.id,
                "event_name": event.name,
                "event_start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "event_end_time": event.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "participants": list(event.participants.values_list('email', flat=True))
            })
            send_to_rabbitmq('event_notifications', message)


def start():
    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(notify_worker, 'interval', seconds=30,id="Notification_Worker",replace_existing=True,name="Notification_Worker",max_instances=1)
    scheduler.start()
    for job in scheduler.get_jobs():
        print(
            f"Job '{job.name}' of type '{job.trigger}' scheduled next to run at: {job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"

result_backend = "redis://localhost:6379/0"

timezone = "Asia/Kolkata"

enable_utc = False

task_serializer = "json"

result_serializer = "json"

accept_content = ["json"]

broker_connection_retry_on_startup = True
task_track_started = True

beat_schedule = {
    "daily-reminder": {
        "task": "tasks.daily_reminder",
        "schedule": crontab(hour=11, minute=1),
    },
    "monthly-report": {
        "task": "tasks.monthly_report",
        "schedule": crontab(hour=11, minute=1, day_of_month=14),
    },
}

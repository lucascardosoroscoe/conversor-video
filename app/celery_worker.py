from celery import Celery
 

celery = Celery("worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery.conf.task_routes = {
    "app.tasks.process_video": {"queue": "video"},
}

from app import tasks 
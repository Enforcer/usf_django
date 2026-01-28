from typing import Any

from celery import Celery, local

from outbox.models import OutboxEntry


def put_in_outbox(task: local.Proxy, **kwargs: Any) -> None:
    """
    task: task function, decorated with @shared_task
    kwargs: any arguments that are passed to the task
    """
    OutboxEntry.objects.create(task_name=task.name, arguments=kwargs)


def flush_outbox(celery_app: Celery) -> None:
    # how to get task object by name:
    # task_name = "..."
    # celery_app[task_name]
    entries = OutboxEntry.objects.all()

import logging
from typing import Any

from celery import Celery, local

from outbox.models import OutboxEntry

logger = logging.getLogger(__name__)


AT_ONCE = 100


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
    entries_qs = OutboxEntry.objects.order_by("-pk")[:AT_ONCE]
    for entry in entries_qs:
        task = celery_app.tasks[entry.task_name]
        try:
            task.delay(**entry.arguments)
        except Exception:
            logger.exception("Error during scheduling task %s!", entry.task_name)

        entry.delete()

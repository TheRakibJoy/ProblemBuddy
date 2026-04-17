"""Start a Codeforces-handle ingestion in the background and track its
progress via a :class:`TrainingJob` row. Works without Celery by using a
daemon thread; if Celery is available the caller can dispatch the task
instead."""

import logging
import threading
import traceback

from django.db import close_old_connections, transaction

from Dataset.add_data import ingest_handle
from Dataset.constants import RATING_TIERS
from Dataset.models import Handle

logger = logging.getLogger(__name__)


def _run_job(job_id: int) -> None:
    from .models import TrainingJob  # deferred to avoid circular imports at startup

    close_old_connections()
    try:
        job = TrainingJob.objects.get(pk=job_id)
    except TrainingJob.DoesNotExist:
        return

    with transaction.atomic():
        job.status = "running"
        job.total = len(RATING_TIERS)
        job.save(update_fields=["status", "total"])

    try:
        Handle.objects.get_or_create(handle=job.handle)
        prev_target = 0
        for i, (_floor, target, tier, label) in enumerate(RATING_TIERS, start=1):
            job.current_tier = label
            job.done = i - 1
            job.save(update_fields=["current_tier", "done", "updated_at"])
            ingest_handle(job.handle, prev_target, target)
            prev_target = target
            close_old_connections()
        job.done = len(RATING_TIERS)
        job.current_tier = ""
        job.status = "success"
        job.save(update_fields=["done", "current_tier", "status", "updated_at"])
    except Exception:
        logger.exception("Training job %s failed", job_id)
        job.status = "failed"
        job.error = traceback.format_exc(limit=3)
        job.save(update_fields=["status", "error", "updated_at"])
    finally:
        close_old_connections()


def start_training_job(job_id: int) -> None:
    thread = threading.Thread(target=_run_job, args=(job_id,), daemon=True)
    thread.start()

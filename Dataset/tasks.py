"""Celery tasks for long-running Codeforces syncs."""

from celery import shared_task

from .add_data import ingest_handle
from .constants import RATING_TIERS
from .models import Handle


@shared_task(bind=True)
def train_handle(self, handle: str) -> dict:
    Handle.objects.get_or_create(handle=handle)
    prev_target = 0
    total = len(RATING_TIERS)
    added_total = 0
    for i, (_floor, target, tier, label) in enumerate(RATING_TIERS, start=1):
        self.update_state(
            state="PROGRESS",
            meta={"tier": tier, "label": label, "done": i - 1, "total": total},
        )
        added_total += ingest_handle(handle, prev_target, target)
        prev_target = target
    return {
        "tier": None,
        "label": "complete",
        "done": total,
        "total": total,
        "added": added_total,
    }

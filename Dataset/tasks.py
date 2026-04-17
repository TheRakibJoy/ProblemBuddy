"""Celery tasks for long-running Codeforces syncs."""

from celery import shared_task

from .add_data import ingest_all_tiers


@shared_task
def train_handle(handle: str) -> None:
    ingest_all_tiers(handle)

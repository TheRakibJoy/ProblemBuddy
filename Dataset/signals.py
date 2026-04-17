"""Invalidate cached per-tier recommender indexes when Problem rows change."""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Problem


@receiver([post_save, post_delete], sender=Problem)
def _invalidate_tier_index(sender, instance: Problem, **kwargs) -> None:
    from Recommender.problem_giver import invalidate_tier_index

    invalidate_tier_index(instance.tier)

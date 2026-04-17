from django.db import models

from .constants import TIER_CHOICES


class Problem(models.Model):
    """A Codeforces problem catalogued under a target rating tier."""

    tier = models.CharField(max_length=32, choices=TIER_CHOICES, db_index=True)
    PID = models.IntegerField()
    Index = models.CharField(max_length=3)
    Rating = models.IntegerField(null=True, db_index=True)
    Tags = models.CharField(max_length=600, null=True)  # noqa: DJ001

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tier", "PID", "Index"], name="unique_problem_per_tier"
            ),
        ]
        indexes = [models.Index(fields=["tier", "Rating"])]

    def __str__(self):
        return f"{self.tier}:{self.PID}{self.Index}"


class Counter(models.Model):
    """Per-tier frequency counter for tags (plus the sentinel 'users' row)."""

    tag_name = models.CharField(max_length=100, db_index=True)
    tier = models.CharField(max_length=32, choices=TIER_CHOICES, db_index=True)
    count = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tag_name", "tier"], name="unique_tag_per_tier"
            ),
        ]

    def __str__(self):
        return f"{self.tag_name}@{self.tier}={self.count}"


class Handle(models.Model):
    handle = models.CharField(max_length=100, null=False, primary_key=True)

    def __str__(self):
        return self.handle

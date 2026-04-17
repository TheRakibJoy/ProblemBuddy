from django.conf import settings
from django.db import models

from Dataset.models import Problem

THEME_CHOICES = [("system", "System"), ("light", "Light"), ("dark", "Dark")]

INTERACTION_STATUS_CHOICES = [
    ("solved", "Solved"),
    ("not_interested", "Not interested"),
    ("hidden", "Hidden"),
]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    cf_handle = models.CharField(max_length=100, unique=True, null=True, blank=True)
    theme_preference = models.CharField(
        max_length=8, choices=THEME_CHOICES, default="system"
    )
    difficulty_offset = models.IntegerField(default=0)
    recommendations_per_load = models.PositiveSmallIntegerField(default=3)

    def save(self, *args, **kwargs):
        self.difficulty_offset = max(-300, min(300, self.difficulty_offset))
        self.recommendations_per_load = max(1, min(12, self.recommendations_per_load))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Profile<{self.user_id}>"


class ProblemInteraction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="problem_interactions",
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="interactions"
    )
    status = models.CharField(max_length=16, choices=INTERACTION_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "problem"], name="unique_user_problem_interaction"
            )
        ]
        indexes = [models.Index(fields=["user", "status"])]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.problem_id}={self.status}"

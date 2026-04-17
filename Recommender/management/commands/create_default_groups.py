from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

DEFAULT_GROUPS = ["contestant", "admin"]


class Command(BaseCommand):
    help = "Create the auth groups ProblemBuddy requires (contestant, admin)."

    def handle(self, *args, **options):
        for name in DEFAULT_GROUPS:
            group, created = Group.objects.get_or_create(name=name)
            verb = "Created" if created else "Already exists:"
            self.stdout.write(f"{verb} group {group.name!r}")

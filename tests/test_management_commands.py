from django.contrib.auth.models import Group
from django.core.management import call_command


def test_create_default_groups(db):
    call_command("create_default_groups")
    assert Group.objects.filter(name="contestant").exists()
    assert Group.objects.filter(name="admin").exists()
    # Idempotent
    call_command("create_default_groups")
    assert Group.objects.filter(name="contestant").count() == 1

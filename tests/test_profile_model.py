import pytest
from django.contrib.auth.models import User

from Recommender.models import Profile


@pytest.mark.django_db
def test_profile_autocreated_on_user_save():
    user = User.objects.create_user(username="alice", password="pw12345!")
    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_profile_clamps_sliders():
    user = User.objects.create_user(username="bob", password="pw12345!")
    profile = user.profile
    profile.difficulty_offset = 9999
    profile.recommendations_per_load = 99
    profile.save()
    profile.refresh_from_db()
    assert profile.difficulty_offset == 300
    assert profile.recommendations_per_load == 12


@pytest.mark.django_db
def test_cf_handle_unique():
    u1 = User.objects.create_user(username="c1", password="pw12345!")
    u2 = User.objects.create_user(username="c2", password="pw12345!")
    u1.profile.cf_handle = "tourist"
    u1.profile.save()
    u2.profile.cf_handle = "tourist"
    with pytest.raises(Exception):
        u2.profile.save()

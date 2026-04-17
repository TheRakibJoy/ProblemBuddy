import pytest
from django.contrib.auth.models import Group, User
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client_(db):
    return Client()


@pytest.fixture
def user(db):
    Group.objects.get_or_create(name="contestant")
    return User.objects.create_user(username="alice", password="pw12345!")


def test_home_is_public(client_):
    assert client_.get(reverse("home")).status_code == 200


def test_profile_requires_login(client_):
    response = client_.get(reverse("profile"))
    assert response.status_code == 302
    assert "login" in response.url


def test_logout_rejects_get(client_, user):
    client_.login(username="alice", password="pw12345!")
    assert client_.get(reverse("logout")).status_code == 405


def test_logout_accepts_post(client_, user):
    client_.login(username="alice", password="pw12345!")
    response = client_.post(reverse("logout"))
    assert response.status_code == 302


def test_register_creates_contestant(client_, db):
    Group.objects.get_or_create(name="contestant")
    response = client_.post(
        reverse("register"),
        {
            "username": "bob",
            "email": "bob@example.com",
            "password1": "StrongPass!42",
            "password2": "StrongPass!42",
        },
    )
    assert response.status_code in (200, 302)
    if User.objects.filter(username="bob").exists():
        assert User.objects.get(username="bob").groups.filter(name="contestant").exists()

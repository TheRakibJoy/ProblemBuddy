from django.contrib import admin
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.urls import path

from Dataset import views as vd
from Recommender import api, views as vr

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", vr.Home, name="home"),
    path("input_handle/", vd.Train, name="train"),
    path("login/", vr.LogIn, name="login"),
    path("logout/", vr.LogOut, name="logout"),
    path("register/", vr.Register, name="register"),
    path("onboarding/", vr.Onboarding, name="onboarding"),
    path("recommender/", vr.Recommend, name="recommend"),
    path("profile/", vr.Profile, name="profile"),
    path("settings/", vr.Settings, name="settings"),
    path(
        "password/change/",
        PasswordChangeView.as_view(template_name="password_change.html"),
        name="password_change",
    ),
    path(
        "password/change/done/",
        PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
        name="password_change_done",
    ),
    # JSON API
    path("api/recommend/", api.recommend_view, name="api_recommend"),
    path("api/interactions/", api.interactions_view, name="api_interactions"),
    path("api/profile/summary/", api.profile_summary_view, name="api_profile_summary"),
    path("api/cf/handle-check/", api.cf_handle_check_view, name="api_cf_handle_check"),
    path("api/settings/", api.settings_view, name="api_settings"),
    path("api/account/delete/", api.account_delete_view, name="api_account_delete"),
    path("api/train/", api.train_enqueue_view, name="api_train_enqueue"),
    path("api/train/active/", api.train_active_view, name="api_train_active"),
    path("api/train/<str:task_id>/", api.train_status_view, name="api_train_status"),
]

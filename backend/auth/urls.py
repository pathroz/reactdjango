# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, SettingsViewPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name="login"),
    path('newstaffaccount/', register_user, name="newstaffaccount"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("settings/<int:pk>/", SettingsViewPage.as_view(), name="settings")
]

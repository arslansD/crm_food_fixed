from django.urls import path

from . import views

urlpatterns = [
    path("roles/", views.RoleViews.as_view(), name="roles"),
    path("users/", views.UserViews.as_view(), name="users"),
    path("registration/", views.RegisterView.as_view(), name="register")
]

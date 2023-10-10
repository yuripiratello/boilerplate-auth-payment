from django.urls import path

from accounts.views import UserRegistrationView, MyTeamView, NewTeamMemberView

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="new-account"),
    path("team/", MyTeamView.as_view(), name="my-team"),
    path("team/add-member", NewTeamMemberView.as_view(), name="new-team-member"),
]

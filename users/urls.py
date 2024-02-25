from django.urls import path
from users.forms import LoginForm
from users.views import CustomLoginView, profile, RegisterView
from .views import verify_email


urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(
            redirect_authenticated_user=True,
            template_name="login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path("register/", RegisterView.as_view(), name="users-register"),
    path("profile/", profile, name="users-profile"),
    path("verify/<str:uidb64>/<str:token>/", verify_email, name="verify_email"),
]

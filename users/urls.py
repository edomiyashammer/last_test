from django.urls import path
from users.forms import LoginForm
from users.views import CustomLoginView, profile, RegisterView

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
    
]

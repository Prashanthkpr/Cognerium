from django.urls import path, include
from users.views.login_register import(
    LoginView
)

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login")
]

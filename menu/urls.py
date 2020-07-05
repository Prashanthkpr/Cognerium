from django.urls import path, include
from menu.views import home
app_name = "menu"

urlpatterns = [
    path('', home, name='home')
]

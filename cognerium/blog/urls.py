from django.urls import path, include
from blog.views import BlogView

app_name = "blog"

urlpatterns = [
	path('posts/', BlogView.as_view(), name='posts')
]
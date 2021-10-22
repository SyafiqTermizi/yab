from django.urls import path

from .views import CreatePostView

app_name = "posts"
urlpatterns = [
    path("create/", CreatePostView.as_view(), name="create"),
]

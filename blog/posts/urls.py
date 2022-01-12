from django.urls import path

from .views import CreatePostView, ListPostView, DetailPostView, upload_image_view

app_name = "posts"
urlpatterns = [
    path("", ListPostView.as_view(), name="list"),
    path("posts/<slug:slug>/", DetailPostView.as_view(), name="detail"),
    path("posts/create/", CreatePostView.as_view(), name="create"),
    path("posts/create/image/", upload_image_view, name="upload_image"),
]

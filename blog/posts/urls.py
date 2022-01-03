from django.urls import path

from .views import CreatePostView, ListPostView, DetailPostView, upload_image_view

app_name = "posts"
urlpatterns = [
    path("create/", CreatePostView.as_view(), name="create"),
    path("<slug:slug>/", DetailPostView.as_view(), name="detail"),
    path("", ListPostView.as_view(), name="list"),
    path("create/image/", upload_image_view, name="upload_image"),
]

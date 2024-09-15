from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("post_detail/<int:post_id>/", views.post_detail, name="post-detail"),
    path("like_post/<int:post_id>/", views.like_post, name="like-post"),
    path("add_comment/<int:post_id>/", views.add_comment, name="add-comment"),
    path(
        "add_reply/<int:post_id>/<int:comment_id>/", views.add_reply, name="add-reply"
    ),
    path(
        "delete_comment/<int:comment_id>/", views.delete_comment, name="delete-comment"
    ),
]

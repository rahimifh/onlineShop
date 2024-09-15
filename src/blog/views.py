from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.dateparse import parse_date

from .forms import CommentForm
from .models import BlogCategory, BlogPost, Comment, Like, Tag


def post_list(request: HttpRequest) -> HttpResponse:
    """
    View to display a list of blog posts.

    This view filters and displays blog posts based on various criteria,
    such as search input, selected category, selected tag, and selected archive month.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered blog post list.

    """

    # Filter and order the blog posts
    posts = BlogPost.objects.filter(status="publish").order_by("-date_published")

    # Get filter criteria from request parameters
    search_input = request.GET.get("search-area") or ""
    selected_category_id = request.GET.get("category") or None
    selected_tag = request.GET.get("tag") or None
    selected_archive = request.GET.get("archive") or None

    # Apply filters based on request parameters
    if search_input:
        posts = posts.filter(title__icontains=search_input)
    elif selected_category_id:
        posts = posts.filter(category=selected_category_id)
    elif selected_tag:
        posts = posts.filter(tag=selected_tag)
    elif selected_archive:
        date = parse_date(selected_archive)
        posts = posts.filter(
            date_published__year=date.year, date_published__month=date.month
        )

    # Pagination
    paginated = Paginator(posts, 9)  # Show up to 9 posts on each page
    page_number = request.GET.get("page")  # Get the requested page number from the URL
    page = paginated.get_page(page_number)
    context = {
        "posts": page.object_list,  # object_list returns posts attached to the page
        "page": page,
        "search_input": search_input,
    }

    return render(request, "blog/post_list.html", context)


# ----------------------------------------------------------------------


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    View to display the detail page of a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the blog post to display.

    Returns:
        HttpResponse: The rendered blog post detail page.

    """
    # Retrieve the specified blog post or show a 404 error if not found
    post = get_object_or_404(BlogPost, pk=post_id)

    if post.status != "publish":
        return HttpResponseNotFound(
            "<h2 style='text-align:center;margin-top:5%;'>این صفحه موجود نیست</h4>"
        )

    comment_form = CommentForm()

    # Get the number of likes for the post
    like_count = Like.objects.filter(post=post).count()

    # Get the comments for the post
    comments = Comment.objects.filter(post=post, status="confirmed")

    # Check if the current user has liked the post
    try:
        is_liked = Like.objects.get(post=post, user=request.user).is_liked
    except Like.DoesNotExist:
        is_liked = None

    context = {
        "post": post,
        "comment_form": comment_form,
        "like_count": like_count,
        "is_liked": is_liked,
        "comments": comments,
        "tags": post.tag.all(),
    }

    return render(request, "blog/post_detail.html", context)


# ----------------------------------------------------------------------


def like_post(request: HttpRequest, post_id: int) -> JsonResponse:
    """
    View to like/unlike a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the blog post to like/unlike.

    Returns:
        JsonResponse: A JSON response indicating the status of the like operation.

    """

    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"data": "You are not authorized yet."}, status=403)

        # Retrieve the specified blog post or show a 404 error if not found
        blog_post = get_object_or_404(BlogPost, id=post_id)

        # Get the 'like_stat' from the POST data, defaulting to False if not provided
        like_stat = request.POST.get("like_stat", False)

        if like_stat == "true":
            # Delete the like if it exists
            Like.objects.filter(post=blog_post, user=request.user).delete()
            return JsonResponse({"like_stat": False}, status=200)
        else:
            # Create a new like
            Like.objects.create(post=blog_post, user=request.user)
            return JsonResponse({"like_stat": True}, status=200)
    else:
        return JsonResponse(status=403)


# ----------------------------------------------------------------------


def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    View to add a comment to a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the blog post to which the comment is added.

    Returns:
        HttpResponseRedirect: A redirection to the blog post detail page after adding the comment.

    """

    post = BlogPost.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.save()
        messages.success(request, "نظر شما ثبت شد و پس از بازبینی منتشر میشود.")
    return redirect(post.get_absolute_url())


# ----------------------------------------------------------------------


def add_reply(request: HttpRequest, post_id: int, comment_id: int) -> HttpResponse:
    """
    View to add a reply to a comment on a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the blog post to which the reply is added.
        comment_id (int): The ID of the comment to which the reply is added. Defaults to None.

    Returns:
        HttpResponseRedirect: A redirection to the blog post detail page after adding the reply.

    """

    post = BlogPost.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_reply = form.save(commit=False)
        new_reply.post = post
        new_reply.reply = comment
        new_reply.status = "confirmed"
        new_reply.is_reply = True
        new_reply.save()
        messages.success(request, "پاسخ شما ثبت شد.")
    return redirect(post.get_absolute_url())


# ----------------------------------------------------------------------


def delete_comment(request: HttpRequest, comment_id: int) -> HttpResponseRedirect:
    """
    View to delete a comment.

    Args:
        request (HttpRequest): The HTTP request object.
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        HttpResponseRedirect: A redirection to the appropriate page after deleting the comment.

    """

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.info(request, "نظر شما حذف شد.")
    else:
        messages.error(request, "شما اجازه حذف این نظر را ندارید.")
    return redirect(comment.post.get_absolute_url())


# ----------------------------------------------------------------------

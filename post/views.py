import os

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from utils.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm, PostForm
from .serializers import PostSerializer, CommentSerializer
# Create your views here.

@login_required
def post_create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, '사진이 등록되었습니다')
            return redirect('post:post_list')
    else:
        post_form = PostForm()

    context = {
        'post_form': post_form,
    }
    return render(request, 'post/post_create.html', context)


def post_list(request):
	posts = Post.objects.all()
	context = {
		'posts': posts,
	}

	return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def comment_create(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            Comment.objects.create(
                post=post,
                author=request.user,
                content=comment_form.cleaned_data['content']
            )
            return redirect('post:post_list')


@login_required
def post_like_toggle(request, post_pk):
    next_path = request.GET.get('next')
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    filtered_like_posts = user.like_posts.filter(pk=post.pk)
    if filtered_like_posts.exists():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)

    if next_path:
        return redirect(next_path)
    return redirect('post:post_detail', post_pk=post_pk)
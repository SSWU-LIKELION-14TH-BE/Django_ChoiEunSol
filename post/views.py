from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostImage, Comment, CommentLike, PostLike
from django.views.decorators.http import require_POST
from django.db.models import Count, F

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        files = request.FILES.getlist('images')

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for file in files:
                PostImage.objects.create(post=post, image=file)

            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'post_create.html', {'form': form})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author:
        post.delete()

    return redirect('post_list')

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    content = request.POST.get('content')
    parent_id = request.POST.get('parent')

    parent = None
    if parent_id:
        parent = Comment.objects.get(id=parent_id)

    Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent=parent
    )

    return redirect('post_detail', pk=pk)

@require_POST
@login_required
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user == comment.author:
        comment.delete()

    return redirect('post_detail', pk=pk)

@login_required
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like, created = PostLike.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect('post_detail', pk=pk)

@login_required
def comment_like_toggle(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment
    )

    if not created:
        like.delete()

    return redirect('post_detail', pk=pk)

def post_list(request):
    posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)

    return render(request, 'post_list.html', {
        'posts': posts,
        'query': query
    })

def post_list(request):
    posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)

    sort = request.GET.get('sort')

    if sort == 'popular':
        posts = posts.annotate(num_likes=Count('likes')).order_by('-num_likes')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'post_list.html', {
        'posts': posts,
        'query': query,
        'sort': sort
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.views = F('views') + 1
    post.save()
    post.refresh_from_db()

    return render(request, 'post_detail.html', {'post': post})
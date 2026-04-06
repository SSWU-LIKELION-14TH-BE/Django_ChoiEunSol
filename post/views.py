from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostImage

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
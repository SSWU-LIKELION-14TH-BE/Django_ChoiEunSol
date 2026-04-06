from django.db import models
from django.conf import settings

class Post(models.Model):
    TECH_CHOICES = [
        ('django', 'Django'),
        ('react', 'React'),
        ('node', 'Node.js'),
        ('spring', 'Spring'),
        ('etc', '기타'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    tech_stack = models.CharField(max_length=20, choices=TECH_CHOICES)
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
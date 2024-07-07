from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blogs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    blog_id = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'
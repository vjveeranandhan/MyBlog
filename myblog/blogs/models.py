from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blogs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
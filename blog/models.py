from django.db import models
from django.utils import timezone

# Create your models here.

class Blog(models.Model):
    name            = models.CharField(max_length=256)
    text            = models.TextField(blank=True, null=True)
    slug            = models.SlugField(max_length=100, blank=True, null=True)
    is_draft        = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    last_modified   = models.DateTimeField(auto_now=True)
    catagories      = models.ManyToManyField('blog.Catagory')

    def __str__(self):
        return self.name
    
    @property
    def day_since_created(self):
        diff = timezone.now() - self.created_date
        return diff.days

class Comment(models.Model):
    blog            = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    text            = models.TextField()
    is_active       = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Catagory(models.Model):
    name        = models.CharField(max_length=256)
    is_active   = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Catagories'

    def __str__(self):
        return self.name

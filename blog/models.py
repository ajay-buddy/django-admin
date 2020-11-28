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

    def __str__(self):
        return self.name
    
    @property
    def day_since_created(self):
        diff = timezone.now() - self.created_date
        return diff.days
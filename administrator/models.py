from django.db import models
from django.utils import timezone
# Create your models here.

class category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True,)
    position = models.IntegerField()
    class Meta:
        ordering = ['position']
    def __str__(self):
        return self.title



class post(models.Model):
    STATUS_CHOICES =(
        ('p', 'publish'),
        ('n', 'draft'),
    )

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField(category, related_name='post')
    dir = models.TextField(max_length=500)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


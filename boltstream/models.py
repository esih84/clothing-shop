# from django.db import models
# from django.conf import settings
#
# from functools import partial
#
# from accounts.models import User
# from django.db.models.signals import post_save
# from django.dispatch import  receiver
# from django.urls import reverse
# from django.utils.crypto import get_random_string
# # Create your models here.
#
# make_stream_key=partial(get_random_string, 20)
#
# class stream(models.Model):
#     user = models.OneToOneField(User,related_name="stream",on_delete=models.CASCADE)
#     key =models.CharField(max_length=20,default=make_stream_key,unique=True)
#     started_at= models.DateTimeField(null=True,blank=True)
#
#     def __str__(self):
#         return self.user.username
#     @property
#     def is_live(self):
#         return self.started_at is not None
#
#     @property
#     def hls_url(self):
#         return reverse("hls-url",args=(self.user.username,))
#     @receiver(post_save,sender=User,dispatch_uid="create_stream_for_user")
#     def create_stream_for_user(sender,instance=None,created=False,**kwargs):
#
#         if created:
#             stream.objects.create(user=instance)
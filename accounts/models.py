from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User,AbstractBaseUser,BaseUserManager
from django.utils import timezone
from django.forms import ModelForm
from django.urls import reverse
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,username,password):
        if not email:
            raise ValueError('please enter an email')

        if not username:
            raise ValueError('please enter an username')

        user = self.model(email = self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self ,email, username, password):
       user = self.create_user(email, username, password)
       user.is_admin = True
       user.save(using=self._db)
       return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_id = models.AutoField(primary_key=True, auto_created=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    private = models.BooleanField(default=False)
    desc = models.TextField(blank=True)
    phone = models.CharField(max_length=11, null=True)
    postal_address = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=200)
    national_code = models.CharField(max_length=10, null=True,)
    follow = models.ManyToManyField(User, related_name='follower', blank=True)
    total_follow = models.IntegerField(default=True)
    unfollow = models.ManyToManyField(User, related_name='unfollow', blank=True)
    total_unfollow = models.IntegerField(default=True)


    def total_follow(self):
        return self.follow.count()

    def total_unfollow(self):
        return self.unfollow.count()
def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = profile(user=kwargs['instance'])
        profile_user.save()

post_save.connect(save_profile_user,sender=User)



class create_post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    desc = models.TextField(max_length=700)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False)
    like = models.ManyToManyField(User, blank=True, related_name='post_like')
    total_like = models.IntegerField(default=True)
    unlike = models.ManyToManyField(User, blank=True, related_name='post_unlike')
    total_unlike = models.IntegerField(default=True)
    def get_absolute_url(self):
        return reverse('accounts:login')

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

class category(models.Model):
    title = models.CharField(max_length=200)
    post = models.ForeignKey(create_post, on_delete=models.CASCADE, null=True, blank=True)

class photo(models.Model):
    post_id = models.ForeignKey(create_post, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='member_images/')


class comment(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    reply = models.ForeignKey("self", related_name='commentid', on_delete=models.CASCADE, blank=True, null=True)
    post_key = models.ForeignKey(create_post, related_name='post_kry', on_delete=models.CASCADE)
    desc = models.TextField(max_length=700)
    date = models.DateTimeField(default=timezone.now)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return self.post_key.name

class comment_form(ModelForm):
    class Meta:
        model = comment
        fields = ['desc']
class reply_form(ModelForm):
    class Meta:
        model = comment
        fields = ['desc']


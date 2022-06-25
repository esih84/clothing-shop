from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import logout
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserProfileUpdate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, views as auth_views
from django.contrib.messages import constants as messages
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.sites.shortcuts import get_current_site


@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out', 'danger')
    return redirect('accounts:login')


def Login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'welcome to your profile', 'success')
            return redirect("accounts:profile")
        else:
            context = {
                "username": username,
                "errormessage": "User not found"
            }
            messages.error(request, 'user or password wrong')
            return render(request, "accounts/login.html")
    else:
        return render(request, 'accounts/login.html', {})


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.user_id) + text_type(timestamp))


email_generator = EmailToken()


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password2'])
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.user_id))

            return redirect('accounts:login')
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@login_required(login_url='/accounts/login/')
def profile_view(request):
    context = {
        'profile': profile.objects.get(user_id=request.user.user_id)

    }
    return render(request, 'accounts/my-account.html', context)


def profile_explore(request, user_id):
    pr = profile.objects.get(user_id=user_id)
    post_usr = create_post.objects.filter(user_id=user_id)
    context = {
        'profile': pr,
        'post': post_usr,
        'photo': photo.objects.all(),
    }
    return render(request, 'accounts/accounts.html', context)


@login_required(login_url='/accounts/login/')
def profile_save(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        user_profile = UserProfileUpdate(request.POST, instance=request.user.profile)
        print(user_profile)
        if user_profile.is_valid() or user_form.is_valid():
            user_form.save()
            user_profile.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('accounts:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        user_profile = UserProfileUpdate(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/update.html', context)


def privat(request):
    if request.method == 'POST':
        user_id = request.user.user_id
        if private.objects.filter(profile_id=user_id).exists():
            private.pr = False
            private.objects.filter(profile_id=user_id).delete()
            messages.success(request, 'your accounts not private', 'dark')
            return redirect('accounts:profile')
        else:
            esi = private.objects.create(profile_id=user_id, pr=True)
            esi.save()
            messages.success(request, 'your accounts is private', 'dark')
            return redirect('accounts:profile')
    else:
        return render(request, 'accounts/settings.html')


@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile')
        else:
            return redirect('accounts:change')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)


def categorys(request, title):
    context = {
         'cater': category.objects.filter(title=title),
    }
    print(context)
    return render(request, 'accounts/category.html', context)



@login_required(login_url='/accounts/login/')
def create_view(request):
    if request.method == "POST":
        if not request.POST['title']:
            raise ValueError("title nust be valid")
        if not request.POST['desc']:
            raise ValueError("desc nust be valid")

        post = create_post.objects.create(user_id=request.user.user_id, title=request.POST['title'],
                                          desc=request.POST['desc'], )
        post.save()

        images = request.FILES.getlist('photo')
        tedad = len(images)
        if tedad > 10:
            messages.success(request, 'Comment left successfully', 'dark')
        for image in images:
            imag = photo.objects.create(photo=image, post_id_id=post.id)
            imag.save()

        cate = category.objects.create(title=request.POST['category'], post_id=post.id)
        cate.save()
        messages.success(request, "Post created successfully", 'success')
    return render(request, 'accounts/create_post.html')


def user_posts(request, user_id):
    context = {
        'userpost': create_post.objects.filter(user_id=user_id),
        'photo': photo.objects.all(),
        'user': request.user.user_id
    }
    return render(request, 'accounts/user_posts.html', context)


def post_detail_view(request, id):
    cate = category.objects.filter(post_id=id)
    phot = photo.objects.filter(post_id_id=id)
    details = get_object_or_404(create_post, id=id)
    commentform = comment_form()
    replyform = reply_form()
    usernam = get_object_or_404(profile, user_id=id)
    context = {
        "cate": cate,
        'phot': phot,
        "replyform": replyform,
        "commentform": commentform,
        "details": details,
        "username": usernam,
        "comment": comment.objects.filter(post_key_id=id, is_reply=False),
    }

    return render(request, 'accounts/posts_detail.html', context)


class delete_post(DeleteView):
    model = create_post
    template_name = "accounts/delete.html"
    success_url = reverse_lazy('accounts:profile')


class edit_view(UpdateView):
    model = create_post
    template_name = "accounts/edit.html"
    fields = ['title', 'desc']


def comments(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        comnents = comment_form(request.POST)
        if comnents.is_valid():
            date = comnents.cleaned_data
            comment.objects.create(desc=date['desc'], user_id=request.user.user_id, post_key_id=id)
            messages.success(request, 'Comment left successfully', 'dark')
            return redirect(url)


def reply(request, id, comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        reply = reply_form(request.POST)
        if reply.is_valid():
            date = reply.cleaned_data
            comment.objects.create(desc=date['desc'], post_key_id=id, user_id=request.user.user_id, reply_id=comment_id,
                                   is_reply=True)
            messages.success(request, 'thanks for reply', 'primary')
            return redirect(url)


def like_view(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(create_post, id=id)
    if product.like.filter(user_id=request.user.user_id).exists():
        product.like.remove(request.user)
        messages.success(request, 'remove', 'dark')
    else:
        product.like.add(request.user)
        messages.success(request, 'add', 'success')
    return redirect(url)


def save_post(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(create_post, id=id)
    if product.save_posts.filter(user_id=request.user.user_id).exists():
        product.save_posts.remove(request.user)
        messages.success(request, 'remove', 'dark')
    else:
        product.save_posts.add(request.user)
        messages.success(request, 'add', 'success')
    return redirect(url)


def save_n(request):
    prudoct = create_post.objects.all()

    context = {
        "post": prudoct,
        "photo": photo.objects.all(),
    }
    return render(request, 'accounts/save.html', context)


def search(request):
    if request.method == 'POST':
        first_name = request.POST['search']
        if first_name:
            search_profile = get_object_or_404(profile, first_name=first_name)
            context = {
                "search_profile": search_profile
            }
            print(search_profile)
            return render(request, 'accounts/searchprofile.html', context)
    else:
        return render(request, 'administrator/index.html', {})


class resetpassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:forgetpassword')
    email_template_name = 'accounts/link.html'


class forgetpassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'


class confirm_password(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:complete')


class complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'


def follwer_follwing_view(request, user_id):
    url = request.META.get('HTTP_REFERER')
    following = get_object_or_404(profile, user_id=user_id)
    if following.follow.filter(user_id=request.user.user_id).exists():
        following.follow.remove(request.user)
        messages.success(request, 'unfollow', 'success')
    else:
        following.follow.add(request.user)
        messages.success(request, 'follow', 'success')
    return redirect(url)


def follower_list(request, user_id):
    following = get_object_or_404(profile, user_id=user_id)
    follower = following.follow.all()
    context = {
        'follower': follower
    }
    return render(request, 'accounts/followers.html', context)


def explore(request):
    context = {
        'post': create_post.objects.all(),
        'photo': photo.objects.all(),
    }
    return render(request, 'accounts/explore.html', context)

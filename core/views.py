import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Posts, Likes, Profile
from .forms import PostsForm, CommentsForm, VotesForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

User = get_user_model()


# Create your views here.
class IndexView(View):
    """
    Index view
    """

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = PostsForm()
        posts = Posts.objects.all()
        votes = Likes.objects.all()
        user = User
        return render(request, "core/index.html", {"posts": posts, "form": form, "votes": votes})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = PostsForm(request.POST, request.FILES)
        posts = Posts.objects.all()
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return render(request, "core/index.html", {"posts": posts, "form": form})
        else:
            return render(request, "core/index.html", {"posts": posts, "form": form})


class PostsDetails(View):
    """
    Posts Details view
    """

    def get(self, request, pk, *args, **kwargs):
        post = Posts.objects.get(id=pk)
        commentForm = CommentsForm()
        voteForm = VotesForm()
        return render(request,
                      "core/post_details.html",
                      {"voteForm": voteForm, "post": post, "commentForm": commentForm})

    def post(self, request, pk, *args, **kwargs):
        commentForm = CommentsForm(request.POST, request.FILES)
        voteForm = VotesForm(request.POST, request.FILES)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user = request.user
            comment.post = Posts.objects.get(id=pk)
            comment.save()
            return redirect("/post/" + str(pk) + "/")
        else:
            return redirect("/post/" + str(pk) + "/")


def voting(request, pk):
    post = Posts.objects.get(id=pk)
    if request.method == 'POST':
        likeForm = VotesForm(request.POST)
        if likeForm.is_valid():
            allLikes = Likes.objects.filter(user=request.user, post=post)
            if len(allLikes) == 0:
                liked = Likes(
                    user=request.user,
                    post=post,
                    design=likeForm.cleaned_data.get("design"),
                    usability=likeForm.cleaned_data.get("usability"),
                    creativity=likeForm.cleaned_data.get("creativity"),
                    content=likeForm.cleaned_data.get("content")
                )
                liked.save()
                return redirect("/post/" + str(pk) + "/")
            print(likeForm.errors)
            return redirect("/post/" + str(pk) + "/")
        return redirect("/post/" + str(pk) + "/")
    return redirect('index')


def profile(request, username):
    title = "profile"
    posts = Posts.get_user(username)
    profile = Profile.get_user(username)
    print(request.user)
    print(profile)
    return render(request, 'core/profile.html', {"title": title, "profiles": profile, "posts": posts})


def update_profile(request, profile_id):
    user = User.objects.get(pk=profile_id)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"You Have Successfully Updated Your Profile!")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'core/update_profile.html', {"u_form": u_form, "p_form": p_form})


def post_site(request):
    current_user = request.user
    print(current_user)
    form = PostsForm(request.POST, request.FILES)
    print(form)
    if form.is_valid():
        print("Valid")
        form = form.save(commit=False)
        form.user = current_user
        form.save()
        print("saved")
        redirect('index_view')
        print("redirecting")
    
    else:
        form = PostsForm()

    return render(request, "core/post_site.html", {"form": form})

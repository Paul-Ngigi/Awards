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
        vote_form = VotesForm()
        return render(request,
                      "core/post_details.html",
                      {"post": post, "commentForm": commentForm, "voteForm": vote_form})

    def post(self, request, pk, *args, **kwargs):
        commentForm = CommentsForm(request.POST, request.FILES)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user = request.user
            comment.post = Posts.objects.get(id=pk)
            comment.save()
            return redirect("/post/" + str(pk) + "/")
        else:
            return redirect("/post/" + str(pk) + "/")


def vote_post(request, id):
    post = Posts.objects.get(id=id)
    likes = Likes.objects.filter(post=post)
    design = []
    usability = []
    creativity = []
    content = []
    for x in likes:
        design.append(x.design)
        usability.append(x.usability)
        creativity.append(x.creativity)
        content.append(x.content)
    de = []
    us = []
    cre = []
    con = []

    if len(usability) > 0:
        usa = (sum(usability) / len(usability))
        us.append(usa)
    if len(creativity) > 0:
        crea = (sum(creativity) / len(creativity))
        cre.append(crea)
    if len(design) > 0:
        des = (sum(design) / len(design))
        de.append(des)
    if len(content) > 0:
        cont = (sum(content) / len(content))
        con.append(cont)

    vote_form = VotesForm()

    if request.method == 'POST':

        vote_form = VotesForm(request.POST)
        if vote_form.is_valid():
            design = vote_form.cleaned_data['design']
            usability = vote_form.cleaned_data['usability']
            content = vote_form.cleaned_data['content']
            creativity = vote_form.cleaned_data['creativity']
            rating = Likes(design=design, usability=usability,
                           content=content, creativity=creativity,
                           user=request.user, post=post)
            rating.save()
            return redirect('/')
    return render(request, 'core/post_details.html',
                  {"post": post, "des": des, "usa": usa, "cont": cont, "crea": crea, "voteForm": vote_form})


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

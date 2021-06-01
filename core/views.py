from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Posts, Likes
from .forms import PostsForm, CommentsForm, VotesForm, ProfileForm

User = get_user_model()


# Create your views here.
class IndexView(View):
    """
    Index view
    """

    def get(self, request, *args, **kwargs):
        form = PostsForm()
        posts = Posts.objects.all()
        return render(request, "core/index.html", {"posts": posts, "form": form})

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

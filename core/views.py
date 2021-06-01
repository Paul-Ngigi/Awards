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

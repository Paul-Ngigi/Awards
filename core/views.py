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


class ProfileView(View):
    """
    profile view
    """

    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        return render(request, "core/profile.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile_view")

from django.urls import path
from .views import IndexView, PostsDetails, voting, ProfileView
from django.contrib.auth.decorators import login_required, permission_required

# Core Urls
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index_view'),  # Url to the home page,
    path('post/<int:pk>/', login_required(PostsDetails.as_view()), name='details_view'),  # Url to the posts details page,
    path('vote/<int:pk>/', login_required(voting), name='votes_view'),  # Url to the vote page,
    path('profile/', login_required(ProfileView.as_view()), name='profile_view'),  # Url to the vote page,
]

from django import forms
from .models import Posts, Profile, Comments, Likes
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'dp']


class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['user']
        fields = ['name', 'description', 'link', 'image1', 'image2', 'image3']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = []
        fields = ['comment']


rating_choices = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
]


class VotesForm(forms.Form):
    design = forms.CharField(label='Design level', widget=forms.RadioSelect(choices=rating_choices))

    usability = forms.CharField(label='Usability level', widget=forms.RadioSelect(choices=rating_choices))

    creativity = forms.CharField(label='Creativity level', widget=forms.RadioSelect(choices=rating_choices))

    content = forms.CharField(label='Content level', widget=forms.RadioSelect(choices=rating_choices))

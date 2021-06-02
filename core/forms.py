from django import forms
from .models import Posts, Profile, Comments, Likes


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ['dp', 'bio', 'phone_number']


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
    class Meta:
        model = Likes
        fields = ['creativity', 'content', 'design', 'usability']

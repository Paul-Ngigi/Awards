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

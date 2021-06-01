from django import forms
from .models import Posts, Profile, Comments, Likes


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ['dp', 'bio', 'phone_number']

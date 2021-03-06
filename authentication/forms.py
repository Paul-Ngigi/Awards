from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()
non_allowed_usernames = []


# Authentication forms
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        user_qs = User.objects.filter(username__iexact=username)

        if not user_qs.exists:
            print("Clean username " + username)
            raise forms.ValidationError("This is an invalid user.")
            return username
        return username


class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


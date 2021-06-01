from django import forms
from django.contrib.auth import get_user_model

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


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username"
            }
        )
    )
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)

        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another one")
        if qs.exists:
            raise forms.ValidationError("This username is already taken.")
            return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)

        if qs.exists:
            raise forms.ValidationError("This email has a registered account")
            return email
        return email

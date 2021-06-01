from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


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

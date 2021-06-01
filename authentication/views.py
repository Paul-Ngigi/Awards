from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.generic import View
from .forms import LoginForm, RegistrationForm
from core.models import Profile

User = get_user_model()


# Create your views here.
class SignUp(View):
    """
    Sign up view
    """
    title = 'signup'

    template_name = 'authentication/signup.html'
    context = {"title": title}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_view')
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")

            try:
                user = User.objects.create_user(username, email, password)
                profile = Profile(user=user)
                profile.save()
            except:
                user = None

            if user != None:
                return redirect('login_view')
            else:
                request.session['register_error'] = 1

        context = {"form": form}
        return render(request, self.template_name, context)

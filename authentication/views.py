from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.generic import View
from .forms import LoginForm, UserForm
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
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')

        return render(request, 'authentication/signup.html', {"form": form})


class Login(View):
    """
    Sign in view
    """
    form = LoginForm()
    template_name = 'authentication/signin.html'

    def get(self, request, *args, **kwargs):
        print("anything1")
        if request.user.is_authenticated:
            print("anything2")
            return redirect('home_view')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        print("anything3")
        if form.is_valid():
            print("anything4")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username)
            print(password)
            if username and password:
                print("anything5")
                user = authenticate(request, username=username, password=password)
                print("anything6")
                if user is not None:
                    print("anything7")
                    login(request, user)
                    print("anything8")
                    return redirect('index_view')

                else:
                    request.session['invalid_user'] = 1

        else:
            print("Error")
        context = {"form": form}
        return render(request, self.template_name, context)


class SignOut(View):
    """
    Sign out view
    """

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login_view')

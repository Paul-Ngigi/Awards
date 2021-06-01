from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.generic import View
from .forms import LoginForm, RegistrationForm

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
                    return redirect('home_view')

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

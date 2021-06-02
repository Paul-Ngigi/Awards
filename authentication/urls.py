from django.urls import path, include
from .views import SignUp, Login, SignOut
from django_registration.backends.one_step.views import RegistrationView

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('login/', Login.as_view(), name='login_view'),
    path('signup/', SignUp.as_view(), name='signup_view'),
    path('signout/', SignOut.as_view(), name='signout_view'),
    path('auth/', include('django_registration.backends.one_step.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/register/',
         RegistrationView.as_view(success_url='/profile/'),
         name='django_registration_register'),
]

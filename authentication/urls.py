from django.urls import path, include
from .views import SignUp, Login, SignOut

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('login/', Login.as_view(), name='login_view'),
    path('signup/', SignUp.as_view(), name='signup_view'),
    path('signout/', SignOut.as_view(), name='signout_view'),
]

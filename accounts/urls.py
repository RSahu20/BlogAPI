
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView

urlpatterns = [
    path('register/',  RegisterView.as_view(), name ='register'),
    path('login/', LoginView.as_view()), # Handle all companies info list
    path('logout/', LogoutView.as_view(), name = "logout"), # Handle all companies info list
    path('change_password/', ChangePasswordView.as_view(), name = "change-password") # Handle all companies info list


]


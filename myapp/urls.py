from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('lecture/detail/<int:pk>', views.lecture_view, name='lecture_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/lecture/<int:pk>/', views.lect_dashboard, name='lect_dashboard')
] 


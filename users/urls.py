from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', views.profile, name='profile'),
    path('list/', views.user_list, name='user_list'),
    path('edit-profile/', views.edit_ptofile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='users/change_password.html', success_url='change_password/'), name='change_password'),
]
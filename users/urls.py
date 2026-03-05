from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', views.profile, name='profile'),
    path('list/', views.user_list, name='user_list'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/change_password.html',
            success_url=reverse_lazy('projects:list')
        ), name='change_password'
    )
]

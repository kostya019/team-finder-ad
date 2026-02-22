from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', views.profile, name='profile'),
    path('list/', views.users_list, name='users_list')
    path('/', include('django.contrib.auth.urls')),
]
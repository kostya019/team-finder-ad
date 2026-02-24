from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', views.profile, name='profile'),
    path('list/', views.user_list, name='user_list'),
    path('/', include('django.contrib.auth.urls')),
]
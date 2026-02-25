from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list , name='list'),
    path('create-project/', views.project_create , name='create'),
    path('<int:project_id>/', views.project_detail , name='detail'),
    path('<int:project_id>/edit/', views.project_create , name='edit'),
    path('<int:project_id>/complete/', views.project_complete , name='complete'), # post при нажатии "Завершить проект"

    path('<int:project_id>/skills/<skill_id>/remove/', views.skill_remove , name='remove_skill'), #post
    path('skills/add/', views.skill_add , name='add'), #post
    path('skills/<str:skill_name>/', views.skill_search , name='search'), #get
]

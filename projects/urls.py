from django.urls import path
from . import views
app_name = 'projects'

urlpatterns = [
    path('projects/list/', views.project_list , name='list'),
    path('projects/create-project/', views.project_create , name='create'),
    path('projects/<int:project_id>/', views.project_detail , name='detail'),
    path('projects/<int:project_id>/edit/', views.project_create , name='edit'),
    path('projects/<int:project_id>/complete/', views.project_complete , name='complete'), # post при нажатии "Завершить проект"

    path('projects/<int:project_id>/skills/<skill_id>/remove/', views.skill_remove , name='remove_skill'), #post
    path('projects/skills/add/', views.skill_add , name='add'), #post
    path('projects/skills/<str:skill_name>/', views.skill_search , name='search'), #get
]

from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='list'),
    path('create-project/', views.project_create, name='create'),
    path('<int:project_id>/', views.project_detail, name='detail'),
    path('<int:project_id>/edit/', views.project_edit, name='edit'),
    path('<int:project_id>/complete/', views.project_complete, name='complete'),
    path('<int:project_id>/toggle-participate/', views.participate, name='participate'),

    path(
        '<int:project_id>/skills/<int:skill_id>/remove/',
        views.skill_remove, name='remove_skill'
    ),
    path('<int:project_id>/skills/add/', views.skill_add, name='add'),
    path('skills/', views.skill_search, name='search'),
]

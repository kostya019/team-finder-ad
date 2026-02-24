from django.shortcuts import render

# Create your views here.

def project_list(request):
    return render(request, "projects/project_list.html")

def project_create(request):
    pass

def project_detail(request, project_id):
    pass

def project_create(request, project_id=-1):
    pass

def project_complete(request, project_id):
    pass

def skill_remove(request, project_id, skill_id):
    pass

def skill_add(request):
    pass

def skill_search(request, skill_name):
    pass

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator

from .models import Project, Skill
from .forms import ProjectForm

def project_list(request):
    all_skills = Skill.objects.all()
    active_skill = request.GET.get('skill')
    
    if active_skill:
        projects = Project.objects.all().filter(skills__name=active_skill)
    else:
        projects = Project.objects.all().filter(status='open')

    # пагинатор на будущее
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': projects,
        'all_skills': all_skills,
        'active_skill': active_skill
    }
    #{"projects": <отфильтрованный queryset проектов>, "all_skills": <все добавленные в БД навыки>, "active_skill": <выбранный фильтр>}
    return render(request, 'projects/project_list.html', context)

@login_required
def project_create(request):
    form = ProjectForm(request.POST or None,)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        form.save()
        return redirect('/projects/list/')
    context = {
        'form': form,
        "is_edit": False
    }
    #{"form": <форма создания/редактирования>, "is_edit": <флаг>}
    return render(request, 'projects/create-project.html', context)

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.is_anonymous or request.user != project.owner:
        return redirect('projects:detail', project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
        return redirect('projects:detail', project_id)

    form = ProjectForm(instance=project)
    context = {
        'form': form,
        "is_edit": True
    }
    return render(request, 'projects/create-project.html', context)

@login_required
def project_complete(request, project_id):
    pass

def project_detail(request, project_id):
    template = 'projects/project-details.html'

    project = get_object_or_404(Project, id=project_id)

    if project is None:
        raise Http404('Error')
    elif project.status == 'closed':
        if project.author != request.user:
            raise Http404('Error')

    context = {
        'project': project,
    }
    return render(request, template, context)

def skill_remove(request, project_id, skill_id):
    pass

def skill_add(request):
    pass

def skill_search(request, skill_name):
    pass

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
import json

from .models import Project, Skill
from .forms import ProjectForm


def project_list(request):
    all_skills = Skill.objects.all()
    active_skill = request.GET.get('skill')

    if active_skill:
        projects = Project.objects.all().filter(
            Q(skills__name=active_skill)
            & Q(status='open')
            )
    else:
        projects = Project.objects.all().filter(status='open')

    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': page_obj,
        'page_obj': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill,
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None,)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        form.save()
        obj.participants.add(obj.owner)
        return redirect('/projects/list/')
    context = {
        'form': form,
        "is_edit": False
    }
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
@require_POST
def project_complete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user == project.owner:
        project.status = 'closed'
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})
    else:
        return JsonResponse({"error": "Permission denied"}, status=403)


@login_required
@require_POST
def participate(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    project = get_object_or_404(Project, id=project_id)

    if project.status == 'closed':
        return JsonResponse({'error': 'Project is closed'}, status=403)

    if project.owner == request.user:
        return JsonResponse({'error': 'Cannot remove owner from participants'}, status=403)

    is_participant = project.participants.filter(id=request.user.id).exists()

    if not is_participant:
        project.participants.add(request.user)
        status = "add"
    else:
        project.participants.remove(request.user)
        status = "remove"

    participants_count = project.participants.count()

    return JsonResponse({
        "status": "ok",
        "participation_status": status,
        "project_id": project_id,
        "participants_count": participants_count,
        "is_participant": not is_participant
    })


def project_detail(request, project_id):
    template = 'projects/project-details.html'

    project = get_object_or_404(Project, id=project_id)

    if project is None:
        raise Http404('Error')
    elif project.status == 'closed':
        if project.owner != request.user:
            raise Http404('Error')

    context = {
        'project': project,
    }
    return render(request, template, context)


@login_required
def skill_add_search_remove(request, project_id=None, skill_id=None):
    q = request.GET.get('q', '').strip()

    # Обработка добавления навыка в проект
    if project_id is not None:
        project = get_object_or_404(Project, id=project_id)

        # Проверка прав доступа: только владелец проекта может вносить изменения
        if request.user != project.owner:
            return JsonResponse({"error": "Permission denied"}, status=403)

        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            if len(body_unicode) == 0:
                skill = get_object_or_404(Skill, id=skill_id)

                # Проверяем, есть ли связь между проектом и навыком
                if skill in project.skills.all():
                    project.skills.remove(skill)  # Удаляем связь через ManyToManyField
                    return JsonResponse({"status": "removed_from_project", "skill_id": skill_id})
                else:
                    return JsonResponse({"error": "Skill not found in project"})

            data = json.loads(body_unicode)
            skill_name_is_data = data.get('name', None)
            skill_id_is_data = data.get('skill_id', None)
            if skill_id_is_data is not None:
                skill = get_object_or_404(Skill, id=skill_id_is_data)
                created = False
            elif skill_name_is_data is not None:
                skill, created = Skill.objects.get_or_create(name=skill_name_is_data.strip())

            # Добавляем связь навыка с проектом
            project.skills.add(skill)
            return JsonResponse({
                "skill_id": skill.id,
                "name": skill.name,
                "created": created,
                "added": True
            })

    # Обработка поиска навыков (автодополнение)
    if not q:
        return JsonResponse([], safe=False)

    skills_queryset = Skill.objects.filter(
        name__istartswith=q
    ).order_by('name')[:10]

    skills_list = [{'id': skill.id, 'name': skill.name} for skill in skills_queryset]
    return JsonResponse(skills_list, safe=False)

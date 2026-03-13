from http import HTTPStatus
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from core.constants import (
    PARTICIPANT_ACTION_ADD,
    PARTICIPANT_ACTION_REMOVE,
    SKILLS_AUTOCOMPLETE_LIMIT,
)
from core.utils import paginate_queryset
from .forms import ProjectForm
from .models import Project, Skill


def project_list(request):
    all_skills = Skill.objects.all()
    active_skill = request.GET.get('skill', '').strip()

    if active_skill:
        projects = Project.objects.all().filter(
            Q(skills__name=active_skill)
            & Q(status='open')
        )
    else:
        projects = Project.objects.all().filter(status='open')

    page_obj = paginate_queryset(projects, request, per_page=12)

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
            messages.success(request, 'Проект успешно обновлён!')
            return redirect(reverse_lazy(
                'projects:detail',
                kwargs={'project_id': project_id}
            ))
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
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
    return JsonResponse({"error": "Permission denied"}, status=HTTPStatus.FORBIDDEN)


@login_required
@require_POST
def participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.status == 'closed':
        return JsonResponse({'error': 'Project is closed'}, status=HTTPStatus.FORBIDDEN)

    if project.owner == request.user:
        return JsonResponse(
            {'error': 'Cannot remove owner from participants'},
            status=HTTPStatus.FORBIDDEN
        )

    is_participant = project.participants.filter(id=request.user.id).exists()

    if not is_participant:
        project.participants.add(request.user)
        status = PARTICIPANT_ACTION_ADD
    else:
        project.participants.remove(request.user)
        status = PARTICIPANT_ACTION_REMOVE

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
        raise Http404('Project does not exist')
    if project.status == 'closed':
        if project.owner != request.user:
            raise Http404('Project is closed')

    context = {
        'project': project,
    }
    return render(request, template, context)


@login_required
def skill_search(request):
    """Поиск навыков для автодополнения."""
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)

    skills = Skill.objects.filter(name__istartswith=q).order_by('name')[:SKILLS_AUTOCOMPLETE_LIMIT]
    results = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(results, safe=False)


@login_required
def skill_add(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        return JsonResponse({"error": "Permission denied"}, status=HTTPStatus.FORBIDDEN)

    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body.decode('utf-8'))
        skill_name = data.get('name', None)
        skill_id = data.get('skill_id', None)

        if skill_id is None and skill_name is None:
            return JsonResponse(
                {"error": "Either 'skill_id' or 'name' must be provided"},
                status=HTTPStatus.BAD_REQUEST
            )

        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)
            created = False
        else:
            skill, created = Skill.objects.get_or_create(name=skill_name.strip())

        project.skills.add(skill)
        return JsonResponse({
            "skill_id": skill.id,
            "name": skill.name,
            "created": created,
            "added": True
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
def skill_remove(request, project_id, skill_id):
    """Удаление навыка из проекта."""
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        return JsonResponse({"error": "Permission denied"}, status=HTTPStatus.FORBIDDEN)

    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    skill = get_object_or_404(Skill, id=skill_id)

    if project.skills.filter(id=skill.id).exists():
        project.skills.remove(skill)
        return JsonResponse({
            "status": "removed_from_project",
            "skill_id": skill_id
        })
    return JsonResponse({"error": "Skill not found in project"}, status=HTTPStatus.NOT_FOUND)

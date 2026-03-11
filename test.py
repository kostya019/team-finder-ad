@login_required
def skill_add_search_remove(request, project_id=None, skill_id=None):
    # Обработка добавления навыка в проект
    if project_id is not None:
        project = get_object_or_404(Project, id=project_id)



        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')

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
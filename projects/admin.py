from django.contrib import admin

from .models import Project, Skill

admin.site.register(Skill)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner',
                    'created_at', 'status')
    list_filter = ('created_at', 'status')
    search_fields = ('name', 'owner', 'created_at', 'description')

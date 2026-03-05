from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('name', 'surname', 'is_active', 'is_staff')

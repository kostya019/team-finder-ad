from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from projects.models import Project
from .forms import CustomAuthenticationForm, CustomUserForm, CustomRegistrationForm
from .models import CustomUser


def profile(request, user_id):
    profile = get_object_or_404(CustomUser, id=user_id)

    if request.user.id != user_id:
        projects = Project.objects.all().filter(
            Q(owner=profile)
            & Q(status='open')
        )
    else:
        projects = Project.objects.all().filter(owner=profile)

    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': profile,
        'page_obj': page_obj
    }
    return render(request, 'users/user-details.html', context)


def user_list(request):
    template = 'users/participants.html'

    users = CustomUser.objects.all().filter(is_active=True).order_by('-id')

    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'participants': page_obj,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def edit_profile(request):
    user = get_object_or_404(CustomUser, id=request.user.id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect(reverse_lazy(
                'users:profile',
                kwargs={'user_id': request.user.id}
            ))
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'users/edit_profile.html', context)


class RegistrationView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = '/projects/list/'

    def form_valid(self, form):
        user = form.get_user()
        if user is not None and user.is_active:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(
                None,
                'Не удалось авторизоваться. Проверьте данные.'
            )
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Передаём request в форму
        return kwargs


@login_required
def custom_logout(request):
    logout(request)
    return redirect('/projects/list/')

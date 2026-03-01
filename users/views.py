from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse

from projects.models import Project
from .forms import CustomAuthenticationForm, CustomUserForm, CustomRegistrationForm
from .models import CustomUser

def profile(request, user_id):
    profile = get_object_or_404(CustomUser, id=user_id)
    context = {'user': profile}
    return render(request, 'users/user-details.html', context)

def user_list(request):
    template = 'users/participants.html'

    users = CustomUser.objects.all().filter(is_active=True).order_by('-id')

    # Пагинатор на будущее
    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "participants": users
    }
    # {"participants": <queryset пользователей>}
    return render(request, template, context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect(reverse_lazy('projects:list'))  # или '/projects/list/'
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'users/edit_profile.html', context)



# В ответ на POST запрос нужно создать нового пользователя в соответствии с полученными данными,
# авторизировать текущего пользователя и переадресовать его на главную страницу (/projects/list).
class RegistrationView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True 
        user.save()
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
            # Обработка случая, когда пользователь не найден или неактивен
            form.add_error(None, 'Не удалось авторизоваться. Проверьте данные.')
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Передаём request в форму
        return kwargs

def custom_logout(request):
    logout(request)
    return redirect('/projects/list/')

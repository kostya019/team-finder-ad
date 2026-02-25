from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from projects.models import Project
from .models import User
from .forms import UserForm


def profile(request, user_id):
    profile = get_object_or_404(User, id=user_id)
    context = {'user': profile}
    return render(request, 'users/user-details.html', context)

def user_list(request):
    template = 'users/participants.html'

    users = User.objects.all().filter(is_active=True).order_by('-id')

    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "participants": page_obj
    }
    return render(request, template, context)

def register(request):
    pass

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None, instance=request.user)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('/projects/list/')

    form = UserForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'users/edit_profile.html', context)


def custom_logout(request):
    logout(request)
    return redirect('/projects/list/')

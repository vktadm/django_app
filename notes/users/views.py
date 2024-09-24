from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def user_login(request):
    """Авторизация пользователя"""
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_app:index')
    context = {'form': form}
    return render(request, 'registration/login.html', context)

def user_logout(request):
    logout(request)
    return render(request,'registration/logged_out.html')

def register(request):
    """Регистрация пользователя"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('main_app:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm

# 1. РЕГИСТРАЦИЯ
def register_view(request):
    """Показывает форму регистрации и обрабатывает её"""

    # Если пользователь УЖЕ вошел, отправляем его на главную
    if request.user.is_authenticated:
        return redirect('main:index')  # 'main:index' — это имя из ваших urls.py

    if request.method == 'POST':
        # ПОЛУЧИЛИ ДАННЫЕ ИЗ ФОРМЫ
        form = RegisterForm(request.POST)

        if form.is_valid():
            # СОХРАНЯЕМ ПОЛЬЗОВАТЕЛЯ
            user = form.save()

            # АВТОМАТИЧЕСКИ ВХОДИМ ПОСЛЕ РЕГИСТРАЦИИ
            login(request, user)

            # ПОКАЗЫВАЕМ СООБЩЕНИЕ ОБ УСПЕХЕ
            messages.success(request, f'Привет, {user.username}! Вы успешно зарегистрировались.')

            # ОТПРАВЛЯЕМ НА ГЛАВНУЮ
            return redirect('main:index')
        else:
            # ЕСЛИ БЫЛИ ОШИБКИ
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        # ПОКАЗЫВАЕМ ПУСТУЮ ФОРМУ
        form = RegisterForm()

    # РЕНДЕРИМ ШАБЛОН С ФОРМОЙ
    return render(request, 'users/register.html', {'form': form})


# 2. ВХОД В АККАУНТ
def login_view(request):
    """Показывает форму входа и обрабатывает её"""

    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # ПОЛУЧАЕМ ДАННЫЕ ИЗ ФОРМЫ
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # ПРОВЕРЯЕМ ЛОГИН/ПАРОЛЬ
            user = authenticate(username=username, password=password)

            if user is not None:
                # ЕСЛИ ВСЁ ВЕРНО — ВХОДИМ
                login(request, user)
                messages.success(request, f'С возвращением, {user.username}!')

                # КУДА ИДТИ ПОСЛЕ ВХОДА
                next_page = request.GET.get('next', 'main:index')
                return redirect(next_page)
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


# 3. ВЫХОД ИЗ АККАУНТА
def logout_view(request):
    """Выход из аккаунта"""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Вы вышли из аккаунта')

    return redirect('main:index')




@login_required
def profile_view(request):
    """Просмотр и редактирование профиля"""
    user = request.user
    message = None

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'users/profile.html', {
        'form': form,
        'user': user
    })

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control glass-card', 'placeholder': 'Введите email'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'email':  # email уже настроен
                field.widget.attrs.update({
                    'class': 'form-control glass-card',
                    'placeholder': f'Введите {field.label.lower()}'
                })


class LoginForm(AuthenticationForm):
    """Форма входа"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control glass-card',
                'placeholder': f'Введите {field.label.lower()}'
            })


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control glass-card',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control glass-card',
                'placeholder': 'Ваша фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control glass-card',
                'placeholder': 'Ваш email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control glass-card',
                'placeholder': '+7 (999) 123-45-67'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем email необязательным для редактирования
        self.fields['email'].required = False


from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя"""
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True)
    address = models.TextField(verbose_name='Адрес', blank=True)
    email_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
    verification_token = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    newsletter_subscription = models.BooleanField(default=True, blank=True, verbose_name='Подписка на рассылку')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
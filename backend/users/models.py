from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name} aka {self.username}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        verbose_name = 'подписку'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author',
                ],
                name='unique_subscription',
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        send_mail(
            'Уведомление о прохождении регистрации на FDGRM',
            f'Привет, {instance.username}! Ты зарегистрировался на нашем '
            'сайте. Добро пожаловать!',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )


signals.post_save.connect(user_post_save, sender=User)

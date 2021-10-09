import asyncio

from django.conf import settings
from django.core.mail import send_mail


class AsyncEmailSender:
    def __init__(self, instance):
        self.instance = instance

    async def main(self):
        await asyncio.get_event_loop().run_in_executor(
            None,
            send_mail,
            'Уведомление о прохождении регистрации на FDGRM',
            f'Привет, {self.instance.username}! Ты зарегистрировался на '
            'нашем сайте. Добро пожаловать!',
            settings.EMAIL_HOST_USER,
            [self.instance.email],
            False
        )

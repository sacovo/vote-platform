from __future__ import absolute_import, unicode_literals

from celery import shared_task

from constance import config
from vote.models import Delegate
from django.core.mail import send_mail


@shared_task
def send_secret_to(delegate_pk, secret):
    delegate = Delegate.objects.get(pk=delegate_pk)

    send_mail(
        config.SUBJECT,
        config.MAIL_TEXT.format(
            secret=secret,
            first_name=delegate.first_name,
            email=delegate.email,
        ),
        config.DEFAULT_FROM_EMAIL,
        [delegate.email],
    )

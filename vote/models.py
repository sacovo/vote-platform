import uuid
import secrets

from django.contrib.auth.hashers import make_password
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


def public_view(secret):
    return secret[:10] + "..." + secret[-10:]


def generate_password():
    return make_password(secrets.token_urlsafe(40))

class Section(models.Model):
    name = models.CharField(max_length=180)

    def __str__(self):
        return self.name


class Delegate(models.Model):
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    street = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    section = models.ForeignKey(Section, models.CASCADE)
    secret = models.CharField(max_length=100, default=generate_password)

    def __str__(self):
        return self.first_name


class Votation(models.Model):
    title = models.CharField(max_length=180)
    description = models.CharField(max_length=300, blank=True)
    options = models.TextField()

    voted = models.ManyToManyField(Delegate, blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    block = models.CharField(max_length=20)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    def get_options(self):
        return [x.strip() for x in self.options.split('\n')]

    def get_choices(self):
        return [(x, x) for x in self.get_options()]

    def get_results(self):
        for option in self.get_options():
            yield option, self.count_votes(option)

    def state(self):
        if self.start_date > timezone.now():
            return _("Geschlossen")
        if self.end_date > timezone.now():
            return _("Offen")
        return _("Abgeschlossen")

    def is_closed(self):
        return self.end_date < timezone.now()

    def is_open(self):
        return not self.is_closed() and\
                self.start_date < timezone.now()

    def count_votes(self, option):
        return self.vote_set.filter(vote=option).count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'votation-detail', kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['block', 'title']


class Vote(models.Model):
    votation = models.ForeignKey(
        Votation, models.CASCADE,
    )

    secret = models.CharField(max_length=80)

    created_at = models.DateTimeField(auto_now_add=True)

    vote = models.CharField(max_length=40)

    section = models.ForeignKey(Section, models.CASCADE)

    def __str__(self):
        return f'{self.votation.title}: {self.vote}'

    class Meta:
        ordering = ['-created_at']

    def public_view(self):
        return public_view(self.secret)

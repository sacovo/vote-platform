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

    valid_choices = models.IntegerField(default=1)
    min_choices = models.IntegerField(default=0)
    add_empty_lines = models.BooleanField(default=False)
    allow_intermediate = models.BooleanField(default=True)
    display_sections = models.BooleanField(default=True)

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
        if self.add_empty_lines:
            others = self.vote_set.filter(voteset__checked=True).exclude(vote__in=self.get_options()).values_list('vote', flat=True).distinct()
            for other in others:
                yield other, self.count_votes(other)
        yield _("Leer"), self.count_votes('-')

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
        return self.vote_set.filter(vote=option, voteset__checked=True).count()

    def checked_votes(self):
        return self.vote_set.filter(voteset__checked=True)

    def vote_count(self):
        return self.vote_set.filter(voteset__checked=True).exclude(vote='-').count()

    def voter_count(self):
        return self.voteset_set.count()

    def absolute_majority(self):
        return int(self.vote_set.filter(voteset__checked=True).exclude(vote='-').count() / self.valid_choices / 2) + 1

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

    vote = models.CharField(max_length=80)

    section = models.ForeignKey(Section, models.CASCADE)
    voteset = models.ForeignKey("VoteSet", models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.votation.title}: {self.vote}'

    class Meta:
        ordering = ['-created_at']

    def public_view(self):
        return public_view(self.secret)


class VoteSet(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    votation = models.ForeignKey(Votation, models.CASCADE)
    checked = models.BooleanField(default=False)

    def votes(self):
        return  '[' + ', '.join(self.vote_set.all().values_list('vote', flat=True)) + ']'

    def __str__(self):
        return self.votation.title + ": " + str(self.id)


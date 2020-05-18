import uuid
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

# Create your models here.

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

    section = models.ForeignKey(Section, models.CASCADE)
    secret = models.CharField(max_length=40, default=uuid.uuid4)

    def __str__(self):
        return self.first_name

    def public_view(self):
        return f'{self.secret_start()}-...-{self.secret_end()}'

    def secret_end(self):
        return self.secret[-12:]

    def secret_start(self):
        return self.secret[:8]

class Votation(models.Model):
    title = models.CharField(max_length=180)
    options = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

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
        ordering = ['start_date']


class Vote(models.Model):
    votation = models.ForeignKey(
        Votation, models.CASCADE,
    )

    delegate = models.ForeignKey(
        Delegate, models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    vote = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.votation.title}: {self.vote}'

    class Meta:
        ordering = ['-created_at']

from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext as _
from django.db import transaction

from django.http.response import HttpResponse

from vote import models
from vote.forms import VoteForm

# Create your views here.


def votation_list_view(request):
    votations = models.Votation.objects.filter(hidden=False)

    return render(request, 'vote/votation_list.html',
                  {'votation_list': votations})


def votation_detail(request, pk):
    votation = get_object_or_404(models.Votation, pk=pk)

    return render(request, 'vote/votation_detail.html', {
        'votation': votation,
    })


def vote_action(request, pk):

    if request.method == 'POST':
        secret = request.POST.get('code', '-').strip()
        email = request.POST.get('email', '')

        delegate = models.Delegate.objects.filter(email__iexact=email)

        if not delegate.exists():
            votation = models.Votation.objects.get(pk=pk)
            form = VoteForm(request.POST, votation=votation)
            return render(request, 'vote/vote_form.html', {
                'form': form,
                'votation': votation,
            })

        delegate = delegate[0]

        if not check_password(secret, delegate.secret):
            votation = models.Votation.objects.get(pk=pk)
            form = VoteForm(request.POST, votation=votation)
            return render(
                request, 'vote/vote_form.html', {
                    'form': form,
                    'votation': votation,
                    'error_code': _("Wrong code."),
                })

    with transaction.atomic():

        votation = models.Votation.objects.select_for_update().get(pk=pk)
        form = VoteForm(votation=votation)

        if request.method == 'POST':
            form = VoteForm(request.POST, votation=votation)

            if form.is_valid() and request.POST.get('confirm') == '1':
                options = form.cleaned_data['options']
                voteset = models.VoteSet.objects.create(
                    votation=votation, checked=not form.cleaned_data['other'])

                if votation.counted_votation:
                    total = len(options)
                    for i, option in options:
                        models.Vote.objects.create(
                            votation=votation,
                            vote=option,
                            count=total - i + 1,
                            secret=form.cleaned_data['code'],
                            section=form.cleaned_data['delegate'].section,
                            voteset=voteset,
                        )
                else:
                    for option in options:
                        models.Vote.objects.create(
                            votation=votation,
                            vote=option,
                            secret=form.cleaned_data['code'],
                            section=form.cleaned_data['delegate'].section,
                            voteset=voteset,
                        )

                if len(options) == 0:
                    models.Vote.objects.create(
                        votation=votation,
                        vote='-',
                        secret=form.cleaned_data['code'],
                        section=form.cleaned_data['delegate'].section,
                        voteset=voteset,
                    )
                votation.voted.add(form.cleaned_data['delegate'])
                votation.save()
                return render(request, 'vote/success.html', {
                    'options': options,
                    'votation': votation,
                })

            if form.is_valid():
                if votation.counted_votation:
                    form.fields['ordered_input'].widget.attrs[
                        'readonly'] = "readonly"
                else:
                    form.fields['options'].widget.attrs['readonly'] = "readonly"
                return render(request, 'vote/confirm.html', {
                    'data': form.cleaned_data,
                    'form': form,
                    'votation': votation,
                })

    return render(request, 'vote/vote_form.html', {
        'form': form,
        'votation': votation,
    })

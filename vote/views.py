from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.db import transaction

from vote import models
from vote.forms import VoteForm

# Create your views here.


def votation_list_view(request):
    votations = models.Votation.objects.all()

    return render(request, 'vote/votation_list.html',{
        'votation_list': votations
    })


def votation_detail(request, pk):
    votation = get_object_or_404(models.Votation, pk=pk)

    return render(request, 'vote/votation_detail.html', {
        'votation': votation,
    })


@transaction.atomic
def vote_action(request, pk):
    votation = models.Votation.objects.select_for_update().get(pk=pk)
    form = VoteForm(votation=votation)

    if request.method == 'POST':
        form = VoteForm(request.POST, votation=votation)

        if form.is_valid() and request.POST.get('confirm') == '1':
            options = form.cleaned_data['options']
            voteset = models.VoteSet.objects.create(votation=votation, checked=not form.cleaned_data['other'])

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

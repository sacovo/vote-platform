from django.shortcuts import render, get_object_or_404, redirect, reverse

from vote.forms import VoteForm
from vote import models
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


def vote_action(request, pk):
    votation = get_object_or_404(models.Votation, pk=pk)
    form = VoteForm(votation=votation)

    if request.method == 'POST':
        form = VoteForm(request.POST, votation=votation)

        if form.is_valid():
            option = form.cleaned_data['option']
            delegate = form.cleaned_data['delegate']
            vote = models.Vote.objects.create(
                votation=votation,
                delegate=delegate,
                vote=option
            )
            return render(request, 'vote/success.html', {
                'vote': vote,
            })

    return render(request, 'vote/vote_form.html', {
        'form': form,
        'votation': votation,
    })

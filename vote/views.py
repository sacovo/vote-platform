from django.shortcuts import get_object_or_404, redirect, render, reverse

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


def vote_action(request, pk):
    votation = get_object_or_404(models.Votation, pk=pk)
    form = VoteForm(votation=votation)

    if request.method == 'POST':
        form = VoteForm(request.POST, votation=votation)

        if form.is_valid() and request.POST.get('confirm') == '1':
            option = form.cleaned_data['option']
            vote = models.Vote.objects.create(
                votation=votation,
                vote=option,
                secret=form.cleaned_data['code'],
            )
            return render(request, 'vote/success.html', {
                'vote': vote,
            })

        if form.is_valid():
            return render(request, 'vote/confirm.html', {
                'data': form.cleaned_data,
                'form': form,
                'votation': votation,
            })

    return render(request, 'vote/vote_form.html', {
        'form': form,
        'votation': votation,
    })

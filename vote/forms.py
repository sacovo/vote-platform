from django import forms
from django.contrib.auth.hashers import check_password

from vote import models


class VoteForm(forms.Form):
    option = forms.ChoiceField(required=True)
    email = forms.EmailField(required=True)
    code = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        self.votation = kwargs.pop('votation')
        super().__init__(*args, **kwargs)
        self.fields['option'].choices = self.votation.get_choices()

    def clean(self):
        cleaned_data = super().clean()
        secret = cleaned_data['code']
        email = cleaned_data['email']
        option = cleaned_data['option']

        if self.votation.is_closed():
            raise forms.ValidationError(
                'Votation closed!'
            )

        if not models.Delegate.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Authentication failed!'
            )

        delegate = models.Delegate.objects.get(
            email__iexact=email
        )

        if not check_password(secret, delegate.secret):
            raise forms.ValidationError(
                'Authentication failed!'
            )
        if option not in self.votation.get_options():
            raise forms.ValidationError(
                'Invalid option!'
            )
        if self.votation.vote_set.filter(secret=secret).exists():
            raise forms.ValidationError(
                'Already voted'
            )
        cleaned_data['delegate'] = delegate

        return cleaned_data

from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import check_password

from vote import models


class VoteForm(forms.Form):
    email = forms.EmailField(required=True)
    code = forms.CharField(widget=forms.PasswordInput, required=True)
    options = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.votation = kwargs.pop('votation')
        super().__init__(*args, **kwargs)
        self.fields['options'].choices = self.votation.get_choices()

        if self.votation.add_empty_lines:
            for i in range(self.votation.valid_choices):
                self.fields[f'add_{i}'] = forms.CharField(label=_(f"Freie Linie {i+1}"), required=False)

        if self.votation.counted_votation:
            del self.fields['options']
            for choice, name in self.votation.get_choices():
                slug = slugify(choice)
                self.fields[slug] = forms.IntegerField(label=choice, required=True)

    def clean(self):
        cleaned_data = super().clean()
        secret = cleaned_data['code']
        email = cleaned_data['email']
        options = cleaned_data.get('options', list())
        cleaned_data['other'] = False


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

        if len(list(option for option in options if option not in self.votation.get_options())) > 0:
            raise forms.ValidationError(
                'Invalid option!'
            )

        if self.votation.counted_votation:
            pass #TODO: Check that every number was taken


        if self.votation.add_empty_lines:
            for i in range(self.votation.valid_choices):
                value = cleaned_data[f'add_{i}']
                if value and value not in options:
                    options.append(value)
                    cleaned_data['other'] = True

        if len(options) > self.votation.valid_choices:
            raise forms.ValidationError(
                f'Only select {self.votation.valid_choices} options'
            )

        if len(options) < self.votation.min_choices:
            raise forms.ValidationError(
                f'At least {self.votation.min_choices} options required'
            )


        if self.votation.vote_set.filter(secret=secret).exists():
            raise forms.ValidationError(
                'Already voted'
            )

        cleaned_data['delegate'] = delegate
        cleaned_data['options'] = options

        return cleaned_data


class MultipleVoteForm(forms.Form):
    pass

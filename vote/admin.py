import csv
import secrets
from io import StringIO

from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils import timezone

from vote import models

# Register your models here.


def export_section_codes(request, queryset):
    field_names = ['section', 'secret']
    response = HttpResponse(
        content_type="text/csv"
    )
    filename = timezone.now().strftime('%Y-%d-%m-%H%M-codes.csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow(
            [obj['section'], obj['code']]
        )
    print(response)
    return response


def send_secret_to(delegate, secret):
    send_mail(
        "[JUSO E-Vote Tool]: Dein Abstimmungscode",
        f"Code: {secret}",
        'evote@juso.ch',
        [delegate.email],
    )


def new_codes(request, queryset):
    codes = []
    for delegate in queryset:
        secret = secrets.token_urlsafe(40)
        delegate.secret = make_password(secret)
        delegate.save()
        codes.append({
            'code': f'{secret[:10]}...{secret[-10:]}',
            'section': delegate.section,
        })
        send_secret_to(delegate, secret)
    messages.add_message(
        request,
        messages.INFO,
        f'{queryset.count()} new codes generated and sent.'
    )
    return export_section_codes(request, codes)

@admin.register(models.Delegate)
class DelegateAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'section',
    ]

    change_list_template = 'vote/delegate_changelist.html'

    fields = [
        'first_name', 'last_name', 'email', 'section', 'city', 'street'
    ]

    list_filter = [
        'section'
    ]

    autocomplete_fields = [
        'section'
    ]

    actions = ['new_codes']

    def get_urls(self):
        urlpatterns = super().get_urls()
        return [
            path(
                'import/',
                self.admin_site.admin_view(
                self.import_delegates
                ),
                name="vote_delegate_import"
            )
        ] + urlpatterns

    def import_delegates(self, request):
        if request.method == 'POST':
            reader = csv.reader(
                StringIO(request.FILES['csv_file'].read().decode())
            )
            next(reader)

            for row in reader:
                if len(row) < 4 or row[3] == '':
                    continue

                section, _ = models.Section.objects.get_or_create(
                    name=row[0]
                )
                models.Delegate.objects.get_or_create(
                    email=row[3],
                    defaults={
                        'first_name': row[1],
                        'last_name': row[2],
                        'section': section,
                    }
                )
            return redirect('admin:vote_delegate_changelist')
        return render(request, 'vote/import_delegates.html', {})

    def new_codes(self, request, queryset):
        return new_codes(request, queryset)

    new_codes.short_description = "Generate and send new codes"


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Votation)
class VotationAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'block']

    list_filter = [
        'block'
    ]

    actions = ['start_votations', 'end_votations', 'start_votations_new_code']

    def start_votations(self, request, queryset):
        queryset.update(
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(minutes=10)
        )
        messages.add_message(
            request, messages.INFO,
            f'{queryset.count()} votations opened'
        )

    def start_votations_new_code(self, request, queryset):
        self.start_votations(request, queryset)
        return new_codes(request, models.Delegate.objects.all())
    start_votations_new_code.short_description = "Start votations, create and send new codes"

    def end_votations(self, request, queryset):
        queryset.update(
            end_date=timezone.now()
        )


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['votation', 'vote']

    readonly_fields = ['secret', 'vote', 'votation']

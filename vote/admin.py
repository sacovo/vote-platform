from django.contrib import admin
from django.core.mail import send_mail
from django.http import HttpResponse
import csv
from django.utils import timezone

from vote import models
# Register your models here.

@admin.register(models.Delegate)
class DelegateAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'section',
    ]

    readonly_fields = ['secret']

    list_filter = [
        'section'
    ]

    autocomplete_fields = [
        'section'
    ]

    actions = ['send_secrets', 'export_section_codes']

    def send_secrets(self, request, queryset):
        for delegate in queryset:
            send_mail(
                "Abstimmungs-code",
                f"Code: {delegate.secret}",
                'info@juso.ch',
                [delegate.email],
            )

    def export_section_codes(self, request, queryset):
        field_names = ['section', 'secret']
        response = HttpResponse(
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename=export.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow(
                [obj.section, f'{obj.public_view()}']
            )
        return response


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Votation)
class VotationAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']

    actions = ['start_votations', 'end_votations']

    def start_votations(self, request, queryset):
        queryset.update(
            start_date = timezone.now(),
            end_date = timezone.now() + timezone.timedelta(minutes=5)
        )

    def end_votations(self, request, queryset):
        queryset.update(
            end_date = timezone.now()
        )



@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['delegate', 'votation', 'vote']

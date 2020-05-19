from django.contrib import admin
from io import StringIO
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import path
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

    change_list_template = 'vote/delegate_changelist.html'

    readonly_fields = ['secret']

    list_filter = [
        'section'
    ]

    autocomplete_fields = [
        'section'
    ]

    actions = ['send_secrets', 'export_section_codes']

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

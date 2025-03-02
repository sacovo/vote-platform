import csv
import secrets
from io import StringIO
from constance import config

from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.conf import settings
from django.utils import timezone

from vote import models, tasks

# Register your models here.


def export_section_codes(request, queryset):
    field_names = ["section", "secret"]
    response = HttpResponse(content_type="text/csv")
    filename = timezone.now().strftime("%Y-%d-%m-%H%M-codes.csv")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([obj["section"], obj["code"]])
    print(response)
    return response


def export_voted_delegates(request, votation):
    field_names = ["section", "first_name", "last_name", "email"]
    response = HttpResponse(content_type="text/csv")
    filename = timezone.now().strftime("%Y-%d-%m-%H%M-delegates.csv")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in votation.voted.all():
        writer.writerow([obj.section.name, obj.first_name, obj.last_name, obj.email])
    return response


def export_not_voted_delegates(request, votation):
    field_names = ["section", "first_name", "last_name", "email"]
    response = HttpResponse(content_type="text/csv")
    filename = timezone.now().strftime("%Y-%d-%m-%H%M-delegates.csv")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    writer = csv.writer(response)

    writer.writerow(field_names)

    for obj in models.Delegate.objects.exclude(
        pk__in=votation.voted.all().values_list("pk", flat=True)
    ):
        writer.writerow([obj.section.name, obj.first_name, obj.last_name, obj.email])
    return response


def new_codes(request, queryset):
    codes = []
    for delegate in queryset:
        secret = secrets.token_urlsafe(40)
        delegate.secret = make_password(secret)
        delegate.save()
        codes.append(
            {
                "code": f"{secret[:10]}...{secret[-10:]}",
                "section": delegate.section,
            }
        )
        tasks.send_secret_to.delay(delegate.pk, secret)
    messages.add_message(
        request, messages.INFO, f"{queryset.count()} new codes generated and sent."
    )
    return export_section_codes(request, codes)


@admin.register(models.Delegate)
class DelegateAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "section",
    ]

    search_fields = ["first_name", "last_name", "email"]

    change_list_template = "vote/delegate_changelist.html"

    fields = ["first_name", "last_name", "email", "section", "city", "street"]

    list_filter = ["section"]

    autocomplete_fields = ["section"]

    actions = ["new_codes", "new_code_unsafe"]

    def get_urls(self):
        urlpatterns = super().get_urls()
        return [
            path(
                "import/",
                self.admin_site.admin_view(self.import_delegates),
                name="vote_delegate_import",
            )
        ] + urlpatterns

    def import_delegates(self, request):
        if request.method == "POST":
            reader = csv.reader(StringIO(request.FILES["csv_file"].read().decode()))
            # section,first_name,last_name,email
            next(reader)

            for row in reader:
                if len(row) < 4 or row[3] == "":
                    continue

                section, _ = models.Section.objects.get_or_create(name=row[0].strip())
                models.Delegate.objects.get_or_create(
                    email=row[3].strip(),
                    defaults={
                        "first_name": row[1].strip(),
                        "last_name": row[2].strip(),
                        "section": section,
                    },
                )
            return redirect("admin:vote_delegate_changelist")
        return render(request, "vote/import_delegates.html", {})

    def new_codes(self, request, queryset):
        return new_codes(request, queryset)

    new_codes.short_description = "Generate and send new codes"

    def new_code_unsafe(self, request, queryset):
        if queryset.count() != 1:
            return
        delegate = queryset[0]
        secret = secrets.token_urlsafe(40)
        delegate.secret = make_password(secret)
        delegate.save()
        messages.add_message(request, messages.INFO, f"new secret: {secret}")

    new_code_unsafe.short_description = "Generate a new code and display it"


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(models.Votation)
class VotationAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "block"]

    list_filter = ["block"]

    fields = [
        "title",
        "description",
        "options",
        "valid_choices",
        "min_choices",
        "add_empty_lines",
        "allow_intermediate",
        "display_sections",
        "show_absolute_majority",
        "show_end_results",
        "counted_votation",
        "hidden",
        "start_date",
        "end_date",
        "block",
    ]

    search_fields = ["title"]

    actions = [
        "start_votations",
        "end_votations",
        "start_votations_new_code",
        "postpone_votations",
        "export_delegates",
        "not_voted_delegates",
        "hide_votes",
        "unhide_votes",
    ]

    def start_votations(self, request, queryset):
        queryset.update(
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(minutes=30),
            hidden=False,
        )
        messages.add_message(
            request, messages.INFO, f"{queryset.count()} votations opened"
        )

    def start_votations_new_code(self, request, queryset):
        self.start_votations(request, queryset)
        return new_codes(request, models.Delegate.objects.all())

    start_votations_new_code.short_description = (
        "Start votations, create and send new codes"
    )

    def end_votations(self, request, queryset):
        queryset.update(end_date=timezone.now())

    def postpone_votations(self, request, queryset):
        queryset.update(
            start_date=timezone.now() + timezone.timedelta(days=365),
            end_date=timezone.now() + timezone.timedelta(days=365, minutes=30),
        )

    def export_delegates(self, request, queryset):
        return export_voted_delegates(request, queryset[0])

    def not_voted_delegates(self, request, queryset):
        return export_not_voted_delegates(request, queryset[0])

    def hide_votes(self, request, queryset):
        queryset.update(hidden=True)

    def unhide_votes(self, request, queryset):
        queryset.update(hidden=False)


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["votation", "vote"]

    search_fields = ["secret"]

    readonly_fields = ["secret", "vote", "votation", "secret", "count"]

    list_filter = ["votation", "vote"]


class VoteInline(admin.TabularInline):
    fields = ["vote", "secret", "count"]
    readonly_fields = ["secret", "count"]
    model = models.Vote
    extra = 0


@admin.register(models.VoteSet)
class VoteSetAdmin(admin.ModelAdmin):
    inlines = [VoteInline]
    list_display = ["uuid", "votation", "votes", "checked"]

    list_filter = ["votation", "checked"]

    list_editable = ["checked"]

    search_fields = ["vote__secret"]

from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe


class ReporterAdmin(
    ImportExportModelAdmin,
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
):
    list_display = (
        "id",
        "contact_name",
        "contact_phone",
        "contact_mail",
        "ohshown_event_link",
    )

    readonly_fields = (
        "id",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "contact_name",
                    "contact_phone",
                    "contact_mail"
                ),
            },
        ),
    )

    def ohshown_event_link(self, obj): 
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:api_ohshownevent_change", args=(obj.ohshown_event_id,)), obj.ohshown_event.display_number
            )
        )

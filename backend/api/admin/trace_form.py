from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe


class TraceFormAdmin(
    ImportExportModelAdmin,
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
):
    list_display = (
        "id",   
        "formatted_trace_type",
        "formatted_age",
        "image_available",
        "other_info",
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
                    "trace_type",
                    "trace_type_text_object",
                    "age_type",
                    "age_number",
                    "image_available",
                    "other_info",
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

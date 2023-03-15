from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe


class CreatureAdmin(
    ImportExportModelAdmin,
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
):
    list_display = (
        "id",
        "display_number",
        "gender",
        "maturity",
        "size",
        "misc_feature_description",
        "ohshown_event_link",
    )

    readonly_fields = (
        "id",
        "display_number",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("id", "display_number"),
                    ("gender", "maturity", "size"),
                    "misc_feature_description",
                    "ohshown_event"
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

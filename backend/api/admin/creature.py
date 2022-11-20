from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin


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
        "ohshown_event_id",
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

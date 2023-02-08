from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin


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

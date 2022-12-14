from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin


class ShownFormAdmin(
    ImportExportModelAdmin,
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
):
    list_display = (
        "id",   
        "ohshown_feeling",
        "human_number",
        "human_behavior",
        "human_behavior_text",
        "distance",
        "bear_behavior",
        "bear_behavior_text",
        "food",
        "food_object",
        "bear_notice",
        "bear_notice_minutes",
        "human_reaction",
        "human_reaction_text",
        "bear_reaction",
        "bear_reaction_text",
        "human_hurt",
        "human_hurt_text",
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
                    "ohshown_feeling",
                    "human_number",
                    "human_behavior",
                    "human_behavior_text",
                    "distance",
                    "bear_behavior",
                    "bear_behavior_text",
                    "food",
                    "food_object",
                    "bear_notice",
                    "bear_notice_minutes",
                    "human_reaction",
                    "human_reaction_text",
                    "bear_reaction",
                    "bear_reaction_text",
                    "human_hurt",
                    "human_hurt_text",
                ),
            },
        ),
    )

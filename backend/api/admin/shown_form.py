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
        "formatted_human_behavior",
        "distance",
        "formatted_bear_behavior",
        "formatted_food",
        "formatted_bear_notice",
        "formatted_human_reaction",
        "formatted_bear_reaction",
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
                    "human_behavior_text_object",
                    "distance",
                    "bear_behavior",
                    "bear_behavior_text_object",
                    "food",
                    "food_text_object",
                    "bear_notice",
                    "bear_notice_minutes",
                    "human_reaction",
                    "human_reaction_text_object",
                    "bear_reaction",
                    "bear_reaction_text_object",
                    "human_hurt",
                    "human_hurt_text",
                ),
            },
        ),
    )

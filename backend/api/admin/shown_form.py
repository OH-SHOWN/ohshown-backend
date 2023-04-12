from api.admin.actions import (
    ExportCsvMixin,
    ExportLabelMixin,
    GenerateDocsMixin,
)

from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe


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

    def ohshown_event_link(self, obj): 
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:api_ohshownevent_change", args=(obj.ohshown_event_id,)), obj.ohshown_event.display_number
            )
        )


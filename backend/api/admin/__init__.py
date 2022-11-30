from django.contrib import admin

from api.models import (
    OhshownEvent,
    Creature,
    Image,
    ReportRecord,
    Reporter,
)
from api.models.ohshown_event import RecycledOhshownEvent
from api.models.document import Document, CETNext, CETReportStatus, GovResponseStatus, FollowUp
from api.models.image import RecycledImage
from api.models.report_record import RecycledReportRecord
from .ohshown_event import OhshownEventAdmin, RecycledOhshownEventAdmin
from .creature import CreatureAdmin
from .reporter import ReporterAdmin
from .image import ImageAdmin, RecycledImageAdmin
from .report_record import ReportRecordAdmin, RecycledReportRecordAdmin
from api.admin.document import (
    DocumentAdmin,
    CETNextAdmin,
    CETReportStatusAdmin,
    GovResponseStatusAdmin,
    FollowUpAdmin,
)

# Register your models here.
admin.register(OhshownEvent)(OhshownEventAdmin)
admin.register(RecycledOhshownEvent)(RecycledOhshownEventAdmin)

admin.register(Creature)(CreatureAdmin)
admin.register(Reporter)(ReporterAdmin)

admin.register(Image)(ImageAdmin)
admin.register(RecycledImage)(RecycledImageAdmin)

admin.register(ReportRecord)(ReportRecordAdmin)
admin.register(RecycledReportRecord)(RecycledReportRecordAdmin)

admin.register(Document)(DocumentAdmin)

admin.register(CETNext)(CETNextAdmin)
admin.register(CETReportStatus)(CETReportStatusAdmin)
admin.register(GovResponseStatus)(GovResponseStatusAdmin)
admin.register(FollowUp)(FollowUpAdmin)

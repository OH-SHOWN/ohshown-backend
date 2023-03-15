from django.db import models

from .mixins import SoftDeleteMixin
from .ohshown_event import OhshownEvent

class Reporter(SoftDeleteMixin):
    id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=50, blank=True, null=True, help_text='聯絡者姓名')
    contact_phone = models.CharField (max_length=15, blank=True, null=True, help_text='聯絡電話')
    contact_mail = models.EmailField(max_length=255, blank=True, null=True, help_text='聯絡信箱')
    ohshown_event = models.ForeignKey(to=OhshownEvent, on_delete=models.CASCADE)
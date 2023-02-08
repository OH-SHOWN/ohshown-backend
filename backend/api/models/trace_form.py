from django.db import models
from django.contrib.postgres.fields import JSONField

from .mixins import SoftDeleteMixin
from ..utils import format_single_choice_options


class TraceForm(SoftDeleteMixin):
    trace_type_list = [
        (0, '糞便'),
        (1, '腳印'),
        (2, '食痕'),
        (3, '折枝'),
        (4, '爪痕'),
        (5, '其他')
    ];

    age_type_list = [
        (0, '新'), (1, '舊'), (2, '不清楚')
    ]

    id = models.AutoField(primary_key=True)
    trace_type = models.IntegerField(
        blank=True, 
        null=True, 
        choices=trace_type_list, 
        help_text='痕跡類型'
    )
    trace_type_text_object = JSONField(
        blank=True, 
        null=True, 
        help_text='痕跡類型-文字補充'
    )
    age_type = models.IntegerField(
        blank=True, 
        null=True, 
        choices=age_type_list,  
        help_text='痕跡新舊類型'
    )
    age_days = models.IntegerField(
        blank=True, 
        null=True, 
        help_text='痕跡出現時間估計/日'
    )
    image_available = models.BooleanField(
        default=False, 
        help_text='是否提供影像檔案'
    )
    other_info = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text='其他補充資訊'
    )

    def formatted_trace_type(self):
        return format_single_choice_options(dict(self.trace_type_list), self.trace_type, self.trace_type_text_object)

    def formatted_age(self):
        if self.age_type == 0:
            return "%s，約 %d 天" % (dict(self.age_type_list).get(self.age_type), self.age_days)
        elif self.age_type == 1:
            return "%s，約 %d 個月" % (dict(self.age_type_list).get(self.age_type), self.age_days)
        else:
            return dict(self.age_type_list).get(self.age_type)

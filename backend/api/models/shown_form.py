from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

from .mixins import SoftDeleteMixin
from ..utils import format_multiple_choice_options


class ShownForm(SoftDeleteMixin):

    human_behavior_list = [
        (0, "行進"),
        (1, "休息"),
        (2, "開車"),
        (3, "煮食/用餐"),
        (4, "工作"),
        (5, "其他"),
    ]

    distance_list = [
        (0, "小於20"),
        (1, "20-50"),
        (2, "50-100"),
        (3, "大於100公尺"),
    ]

    bear_behavior_list = [
        (0, "慢步"),
        (1, "奔跑"),
        (2, "爬樹"),
        (3, "休息"),
        (4, "覓食"),
        (5, "其他"),
    ]

    food_list = [
        (0, "不清楚"),
        (1, "果實"),
        (2, "莖葉"),
        (3, "蜂蜜"),
        (4, "昆蟲"),
        (5, "動物"),
        (6, "垃圾/廚餘"),
        (7, "家禽/畜"),
        (8, "動物飼料"),
        (9, "農作物"),
        (10, "其他"),
    ]

    bear_notice_list = [
        (0, "黑熊一直未發現我"),
        (1, "目擊前黑熊就發現我了"),
        (2, "目擊後約X分鐘黑熊發現我的存在"),
    ]

    human_reaction_list = [
        (0, "靜止不動"),
        (1, "緩慢離開"),
        (2, "快速逃跑"),
        (3, "爬樹"),
        (4, "使用防熊噴霧"),
        (5, "大聲喊叫或發出聲響"),
        (6, "趴在地上裝死"),
        (7, "拿可防身物品威嚇"),
        (8, "其他"),
    ]

    bear_reaction_list = [
        (0, "繼續原先的活動"),
        (1, "緩慢走開"),
        (2, "吼叫威嚇"),
        (3, "站立"),
        (4, "朝人觀望、戒備"),
        (5, "快速逃離"),
        (6, "主動接近人"),
        (7, "其它"),
    ]

    id = models.AutoField(primary_key=True)
    ohshown_feeling = models.CharField(
        blank=True, 
        null=True, 
        max_length=255, 
        help_text='看到熊當下，目擊者的感覺'
    )
    human_number = models.IntegerField(
        blank=True, 
        null=True, 
        help_text='目擊熊當下人數'
    ) 
    human_behavior = models.IntegerField(
        blank=True, 
        null=True, 
        choices=human_behavior_list, 
        help_text='目擊當下目擊者在做什麼'
    )
    human_behavior_text_object = JSONField(
        blank=True, 
        null=True, 
        help_text='目擊當下目擊者在做什麼-文字補充'
    )
    distance = models.IntegerField(
        blank=True, 
        null=True, 
        choices=distance_list, 
        help_text='目擊者與熊之間的距離'
    )
    bear_behavior = models.IntegerField(
        blank=True, 
        null=True, 
        choices=bear_behavior_list, 
        help_text='目擊當下熊在做什麼'
    )
    bear_behavior_text_object = JSONField(
        blank=True, 
        null=True, 
        help_text='目擊當下熊在做什麼-文字補充'
    )
    food = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=food_list, 
            help_text='黑熊在吃什麼'
        )
    )
    food_text_object = JSONField(
        blank=True, 
        null=True,
        help_text='黑熊在吃什麼-文字補充'
    ) 
    bear_notice = models.IntegerField(
        blank=True, 
        null=True, 
        choices=bear_notice_list, 
        help_text='黑熊何時注意到人員存在'
    )
    bear_notice_minutes = models.IntegerField(
        blank=True, 
        null=True, 
        help_text='目擊後約X分鐘黑熊發現人員存在-X數字'
    )
    human_reaction = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=human_reaction_list, 
            help_text='目擊黑熊後，目擊者反應'
        )
    )
    human_reaction_text_object = JSONField(
        blank=True, 
        null=True, 
        help_text='目擊黑熊後，目擊者反應-文字補充'
    )
    bear_reaction = ArrayField(
        models.IntegerField(
            blank=True, 
            null=True, 
            choices=bear_reaction_list, 
            help_text='黑熊發現目擊者後，黑熊的反應'
        )
    )
    bear_reaction_text_object = JSONField(
        blank=True, 
        null=True, 
        help_text='黑熊發現目擊者後，黑熊的反應-文字補充'
    )
    human_hurt = models.BooleanField(
        blank=True, 
        null=True, 
        help_text='是否有人受傷或意外發生'
    )
    human_hurt_text = models.CharField(
        blank=True, 
        null=True, 
        max_length=255, 
        help_text='是否有人受傷或意外發生-文字補充'
    )

    def formatted_food(self):
        return format_multiple_choice_options(dict(self.food_list), self.food, self.food_text_object)
    def formatted_human_behavior(self):
        return format_multiple_choice_options(dict(self.human_behavior_list), self.human_behavior, self.human_behavior_text_object)
    def formatted_human_reaction(self):
        return format_multiple_choice_options(dict(self.human_reaction_list), self.human_reaction, self.human_reaction_text_object)
    def formatted_bear_reaction(self):
        return format_multiple_choice_options(dict(self.bear_reaction_list), self.bear_reaction, self.bear_reaction_text_object)
    def formatted_bear_behavior(self):
        return format_multiple_choice_options(dict(self.bear_behavior_list), self.bear_behavior, self.bear_behavior_text_object)

from django.db import models


# Create your models here.

class Details(models.Model):
    update_time = models.DateTimeField(auto_now_add=True),
    province = models.CharField(max_length=15, default="无", verbose_name='省')
    city = models.CharField(max_length=15, default="无", verbose_name='市')
    confirm = models.IntegerField(default=0, verbose_name='累计确诊')
    confirm_add = models.IntegerField(default=0, verbose_name='新增确诊')
    heal = models.IntegerField(default=0, verbose_name='累计治愈')
    dead = models.IntegerField(default=0, verbose_name='累计死亡')

    class Meta:
        verbose_name = "Details数据信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.province


# 准备人物列表信息的模型类
class History(models.Model):
    ds = models.DateTimeField(auto_now_add=True),
    confirm = models.IntegerField(default=0, verbose_name='累计确诊')
    confirm_add = models.IntegerField(default=0, verbose_name='当日新增确诊')
    suspect = models.IntegerField(default=0, verbose_name='剩余疑似')
    suspect_add = models.IntegerField(default=0, verbose_name='当日新增疑似')
    heal = models.IntegerField(default=0, verbose_name='累计治愈')
    heal_add = models.IntegerField(default=0, verbose_name='当日累计治愈')
    dead = models.IntegerField(default=0, verbose_name='累计死亡')
    dead_add = models.IntegerField(default=0, verbose_name='当日累计死亡')

    class Meta:
        verbose_name = "History数据信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ds

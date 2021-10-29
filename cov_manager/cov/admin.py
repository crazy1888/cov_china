from django.contrib import admin

from .models import Details, History


# Register your models here.

class DetailsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'update_time', 'province', 'city', 'confirm', 'confirm_add', 'heal', 'dead']


class HistoryInfoAdmin(admin.ModelAdmin):
    list_display = ['ds', 'confirm', 'confirm_add', 'suspect', 'suspect_add', 'heal', 'heal_add', 'dead', 'dead_add']


admin.site.register(Details, DetailsInfoAdmin)
admin.site.register(History, HistoryInfoAdmin)

# admin.site.site_header="数据展示系统"
# admin.site.site_title="商品数据"
admin.site.index_title = "欢迎使用"

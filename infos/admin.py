from django.contrib import admin

from .models import InfosConfig, Patient

admin.site.site_header = '中山大学孙逸仙纪念医院'
admin.site.site_title = '后台管理'

# Register your models here.
@admin.register(InfosConfig)
class InfosConfigadmin(admin.ModelAdmin):
    # 二选一
    # fields = ['pk_id', 'key', 'value', 'comments', 'version', 'source', 'deleted_flag', 'create_time', 'deleted_time']
    list_display = ('pk_id', 'key', 'value', 'comments', 'version', 'source', 'effective_flag'
                    , 'create_time', 'deleted_time')
    list_filter = ('deleted_flag',)
    search_fields = ['key', ]
    ordering = ('pk_id', 'create_time', 'version')
    list_per_page = 10


# admin.site.register(InfosConfig, InfosConfigadmin)


@admin.register(Patient)
class Patientadmin(admin.ModelAdmin):
    list_display = ('pk_id', 'name', 'age', 'addr')
    search_fields = ['key', ]
    list_filter = ('deleted_flag', 'book_flag', 'in_flag', 'out_flag')
    ordering = ('pk_id',)
    list_per_page = 10

# admin.site.register(Patient, Patientadmin)

from django.db import models
from django.utils.html import format_html

# Create your models here.


# # Infos配置文件
class InfosConfig(models.Model):
    pk_id = models.AutoField("配置文件主键", max_length=32, primary_key=True)
    # 以下三列分别存入配置的名称,属性,以及说明
    key = models.CharField('属性', max_length=128, null=False)
    value = models.CharField('属性值', max_length=128, null=False)
    comments = models.CharField('备注', max_length=256, null=True)
    version = models.CharField('版本号', max_length=8, null=False)
    source = models.CharField('来源', max_length=128, null=False)
    create_time = models.DateTimeField('创建时间', null=True)
    deleted_flag = models.BooleanField('删除标识', default=False, null=False)
    deleted_time = models.DateTimeField('删除时间', blank=True, null=True)

    def effective_flag(self):
        return format_html('<span style="color:#ff0000;">{}</span>', '已删除') if self.deleted_flag \
            else format_html('<span style="color:#00ff00;">{}</span>', '正常')

    effective_flag.short_description = '删除标识'
    # # 后台点击保存操作
    # def save(self, *args, **kwargs):
    #     self.key = self.
    #     super().save(*args, **kwargs)


# 患者住院,门诊,预约信息
class Patient(models.Model):
    sex_type = (
        ('1', '男'), ('4', '女'), ('9', '未知')
    )
    pk_id = models.BigAutoField('主键', primary_key=True)
    name = models.CharField('患者姓名', max_length=128, null=False)
    age = models.IntegerField('年龄', default=0, null=False)
    ID = models.CharField("身份证号码", max_length=32, null=False)
    addr = models.CharField('地址', max_length=256, null=False)
    sex = models.CharField("性别", max_length=2, choices=sex_type)
    out_flag = models.BooleanField("门诊标识", default=False)
    out_time = models.DateTimeField('看诊登记时间', blank=True)
    in_flag = models.BooleanField("住院标识", default=False)
    in_time = models.DateTimeField('住院时间', blank=True)
    end_time = models.DateTimeField('出院时间', blank=True)
    book_flag = models.BooleanField("预约标识", default=False)
    book_time = models.DateTimeField('预约看诊时间', blank=True)
    pre_time = models.DateTimeField('预约登进士时间', blank=True)
    deleted_flag = models.BooleanField("记录删除标识", default=False)
    deleted_time = models.DateTimeField('删除时间', blank=True)
    dept_code = models.CharField('科室编码', max_length=10, null=False)
    dept_name = models.CharField('科室名称', max_length=32, null=False)
    doc_code = models.CharField('医生编码', max_length=10, null=False)
    doc_name = models.CharField('医生姓名', max_length=32, null=False)
    create_time = models.DateTimeField('创建时间', null=True)

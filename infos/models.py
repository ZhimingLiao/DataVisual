from django.db import models

# Create your models here.


# Infos配置文件
class InfosConfig(models.Model):
    pk_id = models.CharField("配置文件主键", max_length=32, primary_key=True)
    # 以下三列分别存入配置的名称,属性,以及说明
    key = models.CharField(max_length=128, null=False)
    value = models.CharField(max_length=128, null=False)
    comments = models.CharField(max_length=256, null=True)
    version = models.CharField(max_length=8, null=False)
    source = models.CharField(max_length=128, null=False)
    create_time = models.DateTimeField(null=False)
    deleted_flag = models.BooleanField(default=False, null=False)


# 患者住院,门诊,预约信息
class Patient(models.Model):
    sex_type = (
        ('1', '男'), ('4', '女'), ('9', '未知')
    )
    pk_id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128, null=False)
    age = models.IntegerField(default=0, null=False)
    ID = models.CharField("身份证号码", max_length=32, null=False)
    addr = models.CharField(max_length=256, null=False)
    sex = models.CharField("性别", max_length=2, choices=sex_type)
    out_flag = models.BooleanField("删除标识", default=False)
    out_time = models.DateTimeField(blank=True)
    in_flag = models.BooleanField("删除标识", default=False)
    in_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    book_flag = models.BooleanField("删除标识", default=False)
    book_time = models.DateTimeField(blank=True)
    pre_time = models.DateTimeField(blank=True)
    deleted_flag = models.BooleanField("删除标识", default=False)
    deleted_time = models.DateTimeField(blank=True)
    dept_code = models.CharField(max_length=10, null=False)
    dept_name = models.CharField(max_length=32, null=False)
    doc_code = models.CharField(max_length=10, null=False)
    doc_name = models.CharField(max_length=32, null=False)

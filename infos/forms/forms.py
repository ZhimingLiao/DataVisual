# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州富力海珠城3810  志明  2019-09-15 16:21
# 当前计算机登录名称 :andy
# 项目名称  :DataVisual
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-09-15 16:21'

from DjangoUeditor.forms import UEditorField
from django import forms
from django.forms import ModelForm

from infos.models import Article


class ContentForm(forms.Form):
    content = UEditorField("描述", initial="abc", width=600, height=800)
    # content = forms.CharField(label="请输入内容:", max_length=128)
    # content = forms.CharField(label="内容", widget=UEditorWidget(width=800, height=500, imagePath='aa', filePath='bb', toolbars={}))


class TestForm(ModelForm):
    class Meta:
        model = Article
        fields = ["content"]


if __name__ == '__main__':
    print("test")

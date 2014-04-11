#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.contrib import admin

from observer.models import DocumentProfile, Layout, Question, LayoutField



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1



# Register your models here.
class LayoutAdmin(admin.ModelAdmin):
  search_fields = ['name']
  inlines = (QuestionInline, )



class LayoutFieldAdmin(admin.ModelAdmin):
  search_fields = ['name']



admin.site.register(DocumentProfile)
admin.site.register(Layout, LayoutAdmin)
admin.site.register(LayoutField, LayoutFieldAdmin)
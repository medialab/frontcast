#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.contrib import admin

from observer.models import Property, DocumentProfile



admin.site.register(Property)
admin.site.register(DocumentProfile)
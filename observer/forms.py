#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from observer.models import Device




class DeviceForm(forms.ModelForm):
  class Meta:
    model = Device
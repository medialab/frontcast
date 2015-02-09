#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from observer.models import Device, Document, WorkingDocument, Tag



class LoginForm(forms.Form):
  username = forms.CharField( label=_('login'), max_length=64 )
  password = forms.CharField( label=_('password'),  max_length=64, widget=forms.PasswordInput(render_value=False ) )



class FullDocumentForm(ModelForm):
  class Meta:
    model = Document
    exclude = ('owner', 'slug', 'tags', 'authors', 'status')



class TagsForm(forms.Form):
  type = forms.ChoiceField(choices=Tag.TYPE_CHOICES)
  tags = forms.RegexField(regex=r'^[\=\.\?\:\/\s\w,\-\_\'\(\)]*$',label=_('tags') )



class DeviceForm(forms.ModelForm):
  class Meta:
    model = Device
    exclude = ()
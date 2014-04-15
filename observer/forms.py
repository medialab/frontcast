#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms


class ProfileForm():

  
  topics = forms.ModelMultipleChoiceField(queryset=BlogTopic.objects.all())
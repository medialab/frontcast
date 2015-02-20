#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.text import slugify

#
#    Truncates a string after a given number of chars keeping whole words.
#    
#    Usage as templatetag:
#        {{ string|truncatesmart }}
#        {{ string|truncatesmart:50 }}
#        # Join the words and return
#
def truncatesmart(value, limit=80):
    
    value = unicode(value).strip() # Make sure it's unicode
    
    if len(value) <= limit:# Return the string itself if length is smaller or equal to the limit
      return value
    
    value = value[:limit] # Cut the string
    words = value.split(' ')[:-1] # Break into words and remove the last
    
    return ' '.join(words) + '...'


#
#    Truncates a string after a given number of chars keeping whole words.
#    
#    Usage as templatetag:
#        {{ string|truncatesmart }}
#        {{ string|truncatesmart:50 }}
#        # Join the words and return
#
def uuslug(model, instance, value, max_length=128):
  slug = slugify(value)[:max_length] # safe autolimiting
  slug_base = slug
  i = 1;

  while model.objects.exclude(pk=instance.pk).filter(slug=slug).count():
    candidate = '%s-%s' % (slug_base, i)
    if len(candidate) > max_length:
      slug = slug[:max_length-len('-%s' % i)]
    slug = re.sub('\-+','-',candidate)
    i += 1

  return slug


#
#    DJANGO USER TO DICT
#    ==============
#
def profiler(user):
  return {
    'id': user.id,
    'username': user.username,
    'is_staff': user.is_staff
  }


#
#    Create some brand new tags and attach them wherever you wish.
#    Multiple tags: spearate values field with comma.
#    This helper will help you.
#    Of course, instance's model should have `tags` as m2m property, and 
#    the Tags form provided MUST have `type` and `tags` fields. 
#    
#    Return <form:TagForm>,<instance>
#
@transaction.atomic
def smarttag(instance, epoxy, TagsForm, replace=False):
  form = TagsForm(epoxy.data)

  if form.is_valid():
    tags = list(set([t.strip() for t in form.cleaned_data['tags'].split(',')]))# list of unique comma separated cleaned tags.
    candidates = []
    for tag in tags:
      t, created = Tag.objects.get_or_create(name=tag, type=form.cleaned_data['type'])
      if replace:
        candidates.append(t)
      else:
        instance.tags.add(t)
        

    if replace:
      instance.tags = candidates
    
  return form, instance
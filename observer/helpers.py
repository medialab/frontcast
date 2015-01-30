#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

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
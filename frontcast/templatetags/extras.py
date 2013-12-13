from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def tag(tags, category):
  try:
    serie = tags[category]
  except KeyError, e:
    return ''

  values = []  
  for tag in serie:
    values.append('<a href="%s?filters={%%22tags__slug%%22:%%22%s%%22}">%s</a>' % (reverse('frontcast_home'), tag.slug, tag.name))

  return ', '.join(values)

@register.filter
def media(attachment):
  if attachment['type']=='image':
    return '<img src="%s"/>' % attachment['src']
  if attachment['type']=='video':
    return '''
      <video id="%s" class="video-js vjs-default-skin"
        controls preload="auto" width="100%%" height="264"
        poster="%s">
       <source src="%s" type='video/mp4' />
      </video>

    ''' % (attachment['id'], attachment['poster'], attachment['src'])
  return ''

@register.simple_tag
def reduce(items, property, value):
  # items is a long list of objects
  # having is p rproperty for each oobjet in items key
  # return a list made of o
  for item in items:
    if item[property]==value: yield item
from django.http import HttpResponse
#
#
#   Storage
#   =======
#
#   Direct storage solution. You only have to login. extension are given as first arg
#
def storage( request, folder=None, index=None, extension=None ):
  filename = '%s.%s' % (index, extension)
  res = HttpResponse()
  return res
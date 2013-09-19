import csv

from django.conf import settings
from walt.models import Assignment, Task

#
#
#   @param user instance of<User>
#
#   @return <Assignment_set>
def get_pending_assignments( user ):
  assignments = Assignment.objects.filter(unit__profile__user=user)
  return assignments


def unicode_dict_reader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])
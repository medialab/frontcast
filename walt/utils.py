from django.conf import settings
from walt.models import Assignment

#
#
#   @param user instance of<User>
#
#   @return <Assignment_set>
def get_pending_assignments( user ):
  assignments = Assignment.objects.filter(unit__profile__user=user)
  return assignments


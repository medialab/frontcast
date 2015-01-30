import logging
from django_auth_ldap.backend import LDAPBackend as _LDAPBackend
from observer.models import Profile



logger = logging.getLogger(__name__)




class LDAPBackend(_LDAPBackend):
  def get_or_create_user(self, username, ldap_user):
    email = ' '.join(ldap_user.attrs['mail'])
    first_name = ' '.join(ldap_user.attrs['givenname'])
    last_name = ' '.join(ldap_user.attrs['sn'])

    logger.debug( ldap_user.attrs )

    user, user_created = super(LDAPBackend, self).get_or_create_user(username, ldap_user)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()

    logger.debug('authenticating user: %s %s <%s>' % (first_name,last_name,email))

    profile, profile_created = Profile.objects.get_or_create(user__username=username, defaults={
      'user':user
    })

    return (user, user_created)

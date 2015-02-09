#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, observer

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.translation import activate

from glue import Epoxy, API_EXCEPTION_AUTH

from observer.models import WorkingDocument


#
# API test suite

class WorkingDocumentTest(TestCase):
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True


  def test_save(self):
    '''
    handle duplicates workindocument. Test UUslug indirectly.
    '''
    # creatin ownership
    u = User(username='Kollective')
    u.save()

    w = WorkingDocument(title=u"Untitled - Hello, World!", owner=u)
    w.save()

    w1 = WorkingDocument(title=u"Untitled - Hello, World!", owner=u)
    w1.save()

    self.assertEqual('%s, %s' % (w.slug, w1.slug, w.owner.username), 'untitled-hello-world, untitled-hello-world-1')
    self.assertEqual(w.owner.username, 'Kollective')



class AuthTest(TestCase):
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.anonymous = AnonymousUser()
    self.user = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin = User(
      username='jacob_admin', email='jacob@…', password='top_secret', is_staff=True)
  

  def test_login_already_authentified(self):
    request = self.factory.post(reverse('observer_login', args=[]))
    request.user = self.user
    request.session = {}

    res = json.loads(observer.api.login_view(request).content) # res is a JSON dict
    
    self.assertEqual(res['status'], 'ok')


  def test_login_missing_credentials(self):
    request = self.factory.post(reverse('observer_login', args=[]))
    request.user = self.anonymous
    request.session = {}

    res = json.loads(observer.api.login_view(request).content)
    
    self.assertEqual(res['status'], 'error')
    # right code
    self.assertEqual(res['code'], API_EXCEPTION_AUTH)
    # missing username
    self.assertEqual('username' in res['error'], True)


  def test_login_invalid_credentials(self):
    request = self.factory.post(reverse('observer_login', args=[]), {'username':'jacob', 'password':'jacob'})
    request.user = self.anonymous
    request.session = {}

    res = json.loads(observer.api.login_view(request).content)
    print res
    self.assertEqual(res['status'], 'error')
    # right code
    self.assertEqual(res['code'], API_EXCEPTION_AUTH)
    # missing username
    self.assertEqual(res['error'], 'invalid credentials')
    

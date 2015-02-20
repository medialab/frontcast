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

from observer.models import WorkingDocument, Document


#
# API test suite
class DocumentTest(TestCase):
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True   

  def test_save(self):
    '''
    handle duplicates document and show how to create blank documents. Test UUslug indirectly.
    '''
    # creatin ownership
    u = User(username='Kollective')
    u.save()

    w = Document(title=u"Untitled - Hello, World!", owner=u, reference="A")
    w.save()

    w1 = Document(title=u"Untitled - Hello, World!", owner=u, reference="B")
    w1.save()

    self.assertEqual('%s, %s' % (w.slug, w1.slug), 'untitled-hello-world, untitled-hello-world-1')
    self.assertEqual(w.owner.username, 'Kollective')



#
# API test biblib, if any
class ProxyReferenceTest(TestCase):
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True   

  def test_service(self):
    '''
    testing biblib service, ifa any has been specified into the local_settings file.
    '''
    if settings.BIBLIB_ENDPOINT is not None:
      request = self.factory.post(reverse('observer_proxy_reference', args=[]), '{"id":1,"jsonrpc":"2.0","method":"metadata_by_rec_ids","params":["forccast",["scpo-icom2040-2013-0004"]]}', content_type='application/json')

      print observer.api.proxy_reference(request).content


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

    self.assertEqual('%s, %s' % (w.slug, w1.slug), 'untitled-hello-world, untitled-hello-world-1')
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
    
    self.assertEqual(res['status'], 'error')
    # right code
    self.assertEqual(res['code'], API_EXCEPTION_AUTH)
    # missing username
    self.assertEqual(res['error'], 'invalid credentials')
    

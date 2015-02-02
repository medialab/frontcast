#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.translation import activate

from glue import Epoxy

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

    self.assertEqual('%s, %s by %s' % (w.slug, w1.slug, w.owner.username), 'untitled-hello-world, untitled-hello-world-1 by Kollective')

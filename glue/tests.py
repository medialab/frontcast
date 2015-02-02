#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.translation import activate

from glue import Epoxy


#
# ##EpoxyTest
# Test epoxy class and that urls are fully functional
# 
class EpoxyTest(TestCase):
  '''
  Test Epoxy functions, cfr glue module
  '''
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.user = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')


  def test_epoxy_basics(self):
    '''
    Test basic url, should answer 'ok' if everything is ok
    '''
    request = self.factory.get('/glue/')
    request.user = self.user
    request.LANGUAGE_CODE = 'en-us'

    result = Epoxy(request)
    self.assertEqual(result.response['status'], 'ok')
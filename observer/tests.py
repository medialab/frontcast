#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import RequestFactory

from observer.models import Layout, LayoutField



class LayoutTest(TestCase):

  # Create your tests here.
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True
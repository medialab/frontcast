#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.translation import activate

from observer.models import DocumentProfile
from walt.models import Document, WorkingDocument



class DocumentProfileTest(TestCase):
  
  def setUp(self):
    activate('en-us')
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob.admin', email='jacob.admin@gmail.com', password='top_secret')
    self.admin.is_staff = True
    
    self.student = User.objects.create_user(
      username='mike.student', email='mike.student@gmail.com', password='top_secret')

    # assing a student production to a student
    self.document, created = Document.objects.get_or_create(title=u"Untitled Student Document!", owner=self.student)
    
    # let's attach the profile to the document
    self.profile, created = DocumentProfile.objects.get_or_create(document=self.document, owner=self.admin, layout=self.layout)

    # let's create at least two tools to be attached in a question
    self.tool_a, created = WorkingDocument.objects.get_or_create(title=u"Untitled - Hello, World Tool!", owner=self.admin, type=WorkingDocument.TOOL)

    self.tool_b, created = WorkingDocument.objects.get_or_create(title=u"A second awesome tool", owner=self.admin, type=WorkingDocument.TOOL)
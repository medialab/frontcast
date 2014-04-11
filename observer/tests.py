#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import RequestFactory

from observer.models import DocumentProfile, Layout, LayoutField, Question
from walt.models import Document, WorkingDocument



class LayoutTest(TestCase):
  
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob.admin', email='jacob.admin@gmail.com', password='top_secret')
    self.admin.is_staff = True
    
    self.student = User.objects.create_user(
      username='mike.student', email='mike.student@gmail.com', password='top_secret')

    # assing a student production to a student
    self.document, created = Document.objects.get_or_create(title=u"Untitled Student Document!", owner=self.student)
    
    # let's tcreate a layout to profile the document
    self.layout, created = Layout.objects.get_or_create(name=u"default document profile")

    # let's attach the profile to the document
    self.profile, created = DocumentProfile.objects.get_or_create(document=self.document, owner=self.admin, layout=self.layout)

    # let's create at least two tools to be attached in a question
    self.tool_a, created = WorkingDocument.objects.get_or_create(title=u"Untitled - Hello, World Tool!", owner=self.admin, type=WorkingDocument.TOOL)

    self.tool_b, created = WorkingDocument.objects.get_or_create(title=u"A second awesome tool", owner=self.admin, type=WorkingDocument.TOOL)
    
    self.field_a, created = LayoutField.objects.get_or_create(question=u"Is it a good site ?", type=LayoutField.BOOLEAN)

    self.field_b, created = LayoutField.objects.get_or_create(
      question=u"What kind of tool has been used to analyse the conteroversy?",
      type=LayoutField.MODEL_CHOICE,
      modelname ='walt.WorkingDocument',
      filters=json.dumps({'type': WorkingDocument.TOOL})
    )

    self.field_c, created = LayoutField.objects.get_or_create(
      question=u"What kind of tool has been used to analyse the conteroversy? You can select more than one",
      type=LayoutField.MODEL_MULTIPLE_CHOICE,
      modelname ='walt.WorkingDocument',
      filters=json.dumps({'type': WorkingDocument.TOOL})
    )


  def fill_layout(self):
    '''
    Helper function, fill self.layout with one question per type, sparse order
    '''
    s_a, created = Question.objects.get_or_create(layout=self.layout, field=self.field_a, section=u"ANALYSIS", slug=u"analysis", position=5)
    s_b, created = Question.objects.get_or_create(layout=self.layout, field=self.field_b, section=u"ANALYSIS", slug=u"analysis", position=2)
    s_c, created = Question.objects.get_or_create(layout=self.layout, field=self.field_c, section=u"ANALYSIS", slug=u"analysis", position=3)


  def test_create_form(self):
    '''
    A simple procedure to check form production from a lyayout.
    Cfr setup + fill_layout methods.
    
    1. create a dummy yes no layoutField (field_a)
    2. create a custom layoutField to serve a question related to a tool (field_b) signleshot
    3. create a single section form to link fields and layout, and retrieve the fields according to a position
    Does the layout respect the position?
    Does the form respect the position?
    Respect!
    '''
    self.fill_layout()

    # let's use the unicode method specified in observer.models.Question class
    self.assertEqual(['%s'%s for s in self.layout.questions.all()], [
      'ANALYSIS/2: ModelChoiceField',
      'ANALYSIS/3: ModelMultipleChoiceField',
      'ANALYSIS/5: BooleanField'
    ])

    # actual form fields (test the get_form method)
    self.assertEqual([k for k in self.layout.get_form().fields.keys()], [
      u'field_analysis_2',
      u'field_analysis_3',
      u'field_analysis_1'
    ])


  def test_fill_form(self):
    '''
    Validate insert according to Layout's dynamic form composition
    '''
    self.fill_layout()

    form = self.layout.get_form(data={'field_analysis_1':False})






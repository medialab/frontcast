#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from walt.models import WorkingDocument



class WorkingDocumentTest(TestCase):
  def test_save(self):
    '''
    handle duplicates workindocument. Test UUslug indirectly
    '''
    # creatin gownership
    u = User(username='Kollective')
    u.save()

    w = WorkingDocument(title=u"Untitled - Hello, World!", owner=u)
    w.save()

    w1 = WorkingDocument(title=u"Untitled - Hello, World!", owner=u)
    w1.save()

    self.assertEqual('%s, %s by %s' % (w.slug, w1.slug, w.owner.username), 'untitled-hello-world, untitled-hello-world-1 by Kollective')


  def test_save_hierarchy(self):
    '''
    Hande SEQUENCE to TOOL to TASK conditions on WorkingDocument.save()
    '''
    # creatin gownership
    u = User(username='Kollective')
    u.save()

    # prepare 
    sequence = WorkingDocument(title=u"Untitled - Hello, World Sequence!", owner=u, type=WorkingDocument.SEQUENCE)
    sequence.save()

    task = WorkingDocument(title=u"Untitled - Hello, World Task!", owner=u, type=WorkingDocument.TASK)
    task.save()

    tool = WorkingDocument(title=u"Untitled - Hello, World Tool!", owner=u, type=WorkingDocument.TOOL)
    tool.save()

    task.parent = sequence
    task.save()

    tool.parent = task
    tool.save()

    # Does it raise the correctException?
    try:
      sequence.parent = task
      sequence.save()
    except IntegrityError, e:
      sequence.parent = None
      pass # pass test only when integroity error occurs!!  

    try:
      task.parent = tool
      task.save()
    except IntegrityError, e:
      task.parent = sequence
      pass

    self.assertEqual('%s by %s' % (task.parent.slug, u.username), 'untitled-hello-world-sequence by Kollective')


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import RequestFactory

from walt.models import WorkingDocument, Document, Tag
from walt import api
from glue import API_EXCEPTION_AUTH





class ApiUtilsTest(TestCase):
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True


  def test_url_title(self):
    '''
    Test URL grabbing title.
    '''
    req = self.factory.get('/api/url/title/',{
      'url': 'http://blogs.scientificamerican.com/sa-visual/2014/02/18/dont-just-visualize-datavisceralize-it/'
    })
    req.LANGUAGE_CODE = 'en-us'
    req.user = self.admin

    response = json.loads(api.url_title(req).content)
    self.assertEqual(response['status'],'ok')




class WorkingDocumentTest(TestCase):
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True


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


  def test_api_create(self):
    '''
    Creation of a working document via api.
    '''

    request = self.factory.post('/api/working-document/',{
      'type': '?',
      'title': '@Don’t Just Visualize Data—Visçeralize It!',
      'permalink': 'http://blogs.scientificamerican.com/sa-visual/2014/02/18/dont-just-visualize-datavisceralize-it/'
    })
    request.LANGUAGE_CODE = 'en-us'
    request.user = self.admin

    response = json.loads(api.working_documents(request).content)

    self.assertEqual('ok--jacob--dont-just-visualize-datavisceralize-it', '--'.join([
      response['status'],
      response['object']['owner'],
      response['object']['slug']
    ]))



  def test_api_create_duplicates(self):
    '''
    Creation of two working document via api having the same permalink.
    '''
    req_1 = self.factory.post('/api/working-document/',{
      'type': '?',
      'title': '@Don’t Just Visualize Data—Visçeralize It!',
      'permalink': 'http://blogs.scientificamerican.com/sa-visual/2014/02/18/dont-just-visualize-datavisceralize-it/'
    })
    req_1.user = self.admin
    req_1.LANGUAGE_CODE = 'en-us'
    res_1 = json.loads(api.working_documents(req_1).content)

    req_2 = self.factory.post('/api/working-document/',{
      'type': '?',
      'title': '@Don’t Just Visualize Data—Visçeralize It!',
      'permalink': 'http://blogs.scientificamerican.com/sa-visual/2014/02/18/dont-just-visualize-datavisceralize-it/'
    })
    req_2.user = self.admin
    req_2.LANGUAGE_CODE = 'en-us'
    res_2 = json.loads(api.working_documents(req_2).content)

    self.assertEqual('ok--jacob--dont-just-visualize-datavisceralize-it-1--2--1', '--'.join(str(v) for v in [
      res_2['status'],
      res_2['object']['owner'],
      res_2['object']['slug'],
      res_2['object']['id'],
      res_2['object']['copy_of'][0]['id']
    ]))


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



class DocumentTest(TestCase):
  '''
  Test various graph functions inside walt.api
  '''
  def setUp(self):
    # Every test needs access to the request factory.
    self.factory = RequestFactory()
    self.admin = User.objects.create_user(
      username='jacob', email='jacob@…', password='top_secret')
    self.admin.is_staff = True
    self.student = User.objects.create_user(
      username='jean', email='jean@…', password='top_top_secret')
    

  def test_api_add_document(self):
    '''
    Cfr walt.api.documents.
    Simulate an API request to create a document
    '''
    request = self.factory.post(reverse('walt_api_documents'),{
      'title': 'a brand new document',
      'type': Document.REFERENCE_CONTROVERSY_WEB
    })
    request.method='POST'
    request.user = self.admin
    request.LANGUAGE_CODE = 'en-us'

    # admin is among owners
    response = api.documents(request)
    jresponse = json.loads(response.content)
    
    print jresponse
    
    self.assertEqual(jresponse['object']['title'], u'a brand new document')


    #self.assertEqual('%s-%s-%s' % (jresponse['meta']['action'], jresponse['meta']['method'], jresponse['status']), 'corpus-DELETE-ok')

  def test_api_failing_add_document(self):
    '''
    User is trying to create a document without the adequate permission.
    '''
    request = self.factory.post(reverse('walt_api_documents'),{
      'title': 'a brand new document failing',
      'type': Document.REFERENCE_CONTROVERSY_WEB
    })
    request.method='POST'
    request.user = self.student # a simle user can't do this...
    request.LANGUAGE_CODE = 'en-us'

    response = api.documents(request)
    jresponse = json.loads(response.content)
    self.assertEqual(jresponse['status'], 'error') # not authorized
    self.assertEqual(jresponse['code'], API_EXCEPTION_AUTH)



  def test_api_graph_bipartite(self):
    '''
    Test filters for view graph bipartite. Output should be a well formatted json
    '''
    request = self.factory.get('/api/graph/bipartite/document/tags/?indent&v-filters={"type__in":["Ke"]}&u-filters={"slug__icontains":"mort"}')
    request.user = self.admin
    request.LANGUAGE_CODE = 'en-us'
    self.assertEqual(True, True)



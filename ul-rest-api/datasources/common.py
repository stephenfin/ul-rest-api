#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

from __future__ import print_function

import lxml.html
import urllib, urllib2

'''
Constants
'''

''' Regexs '''
# All regexs generated using the gSkinner RegExr online tool: 
#   http://gskinner.com/RegExr/
COURSE_NAME_RE = '(?P<code>\w+)\s+-(?P<name>(\s+\w+)*)'
SEM_TIME_WKS_RE = 'Wks:((?P<p1_start>\d+)-(?P<p1_end>\d+)),?((?P<p2_start>\d+)-(?P<p2_end>\d+))?'

'''
Definitions
'''

def get_page(url, params=None):
  """
  Retrieves page and creates lxml object

  Uses urlfetch as defined here:
    https://developers.google.com/appengine/docs/python/urlfetch/overview

  @param url: The URL of page to retrieve
  @type url: String
  @param params: List of params to submit to page
  @type url: Dict
  """

  # Handle POST requests
  if (params):
    form_data = urllib.urlencode(params)
    request = urllib2.Request(url = url, data = form_data)
  # Handle GET requests
  else:
    request = urllib2.Request(url = url)

  request.add_header('User-Agent', 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0')

  '''
  #Google method
  reponse - urlfetch.fetch(url = url,
    payload = form_data,
    method = urlfetch.POST,
    headers = {'Content-Type': 'application/x-www-form-urlencoded'})
  '''

  response = urllib2.urlopen(request)

  #Build lxml object from retieved page
  document = lxml.html.parse(response)

  return document

def tidy_tag(tag):
  """
  Get text content of tag and tidy it

  @param tag: The tag to get text content of an tidy
  @type tag: lxml.html.HtmlElement
  """
  return tag.text_content().replace(u'\xa0', ' ').strip().title()
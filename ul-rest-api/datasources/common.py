#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" common.py: Collection of common functions and constants for datasources """

from __future__ import print_function
from collections import OrderedDict

# if running on google app engine
try:
  from google.appengine.api import urlfetch
except ImportError:
  pass

import StringIO
import datetime
import lxml.html
import json
import urllib, urllib2

'''
Constants
'''

API_VERSION = "1.0"

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

  @param url: The URL of page to retrieve
  @type url: String
  @param params: List of params to submit to page
  @type url: Dict
  """

  try:
    from google.appengine.api import urlfetch
  
  # if not running on google app engine
  except ImportError:
    # Handle POST requests
    if (params):
      form_data = urllib.urlencode(params)
      request = urllib2.Request(url = url, data = form_data)
    # Handle GET requests
    else:
      request = urllib2.Request(url = url)

    response = urllib2.urlopen(request)

  # if running on google app engine
  else:
    form_data = None

    # Handle POST requests
    if (params):
      form_data = urllib.urlencode(params)
      method = urlfetch.POST
    # Handle GET requests
    else:
      method = urlfetch.GET

    response = urlfetch.fetch(url=url,
      payload=form_data,
      method=method,
      validate_certificate=False)

    response = StringIO.StringIO(response.content)

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
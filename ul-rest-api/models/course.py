#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" course.py: Datasources for the course services """

from google.appengine.api import memcache
from google.appengine.ext import ndb
import re

from ..datasources.course import module

class Course(ndb.Model):
  def validate_code(self, value):
    ''' Validates a course code '''
    if not re.match(r"[A-Za-z]{2}[0-9]{4}", value):
      raise ValueError
    return value

  code = ndb.StringProperty(validator=validate_code)
  name = ndb.StringProperty()
  url = ndb.StringProperty()

class Module(ndb.Model):
  def validate_code(self, value):
    ''' Validates a course code '''
    if not re.match(r"[A-Za-z]{2}[0-9]{4}", value):
      raise ValueError
    return value

  code = ndb.StringProperty(validator=validate_code)
  name = ndb.StringProperty()

  @classmethod
  def get_module(cls, code):
    module = cls.query(cls.code == code).get()

    if module:
      return module

    result = datasources.course(code)

    if result == -1:
      return None

    module = Module(
      code = result['code'],
      name = result['name'])
    module.put()

    return module
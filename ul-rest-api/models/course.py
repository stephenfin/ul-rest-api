#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" course.py: Model for the course services """

from __future__ import print_function
from collections import OrderedDict
from google.appengine.api import memcache
from google.appengine.ext import ndb
from import_relative import import_relative
import re, os

common = import_relative('common', '..datasources')
course = import_relative('course', '..datasources')

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

    result = course.module(code)

    if result == -1:
      return None

    module = Module(
      code = result['code'].lower(),
      name = result['name'])
    module.put()

    return module

  @classmethod
  def get_module_dict(cls, code):
    module = cls.get_module(code)

    if not module:
      return -1

    data = OrderedDict([
      ('kind', 'module'),
      ('code', module.code),
      ('name', module.name),
    ])

    return data

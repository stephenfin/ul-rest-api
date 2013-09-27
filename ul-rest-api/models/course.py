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
  """ Models a course for UL """
  def validate_code(self, value):
    """ Validates a course code """
    if not re.match(r"[A-Za-z]{2}[0-9]{3}", value):
      raise ValueError
    return value

  code = ndb.StringProperty(validator=validate_code)
  name = ndb.StringProperty()
  url = ndb.StringProperty()

  @classmethod
  def get_course(cls, course_code):
    """
    Gets a course object from datastore.
    
    Attempts to get a course from the datastore. If it is not found, attempt 
    to retrieve details of said course from UL website and add the course to 
    the database before returning this course.

    @param course_code: Course code to get details for
    @type course_code: String

    @return An object of type Course for the course, or None if match not found
    """
    result = cls.query(cls.code == course_code).get()

    if result:
      return result

    result = course.course(course_code)

    if result == -1:
      return None

    new_course = Course(
      code = result['code'].lower(),
      name = result['name'])
    new_course.put()

    return new_course

  @classmethod
  def get_course_dict(cls, course_code):
    """
    Gets a course details as an OrderedDict from datastore.
    
    Attempts to get a course from the datastore. If it is not found, attempt 
    to retrieve details of said course from UL website and add the course to 
    the database before returning this course.

    @param module_code: Course code to get details for
    @type module_code: String

    @return An OrderedDict containing the course code and name, or -1 if match 
    not found
    """
    result = cls.get_course(course_code)

    if not result:
      return -1
      
    data = OrderedDict([
      ('kind', 'course'),
      ('code', result.code),
      ('name', result.name),
    ])

    return data


class Module(ndb.Model):
  """ Models a module for UL """
  def validate_code(self, value):
    """ Validates a course code """
    if not re.match(r"[A-Za-z]{2}[0-9]{4}", value):
      raise ValueError
    return value

  code = ndb.StringProperty(validator=validate_code)
  name = ndb.StringProperty()

  @classmethod
  def get_module(cls, module_code):
    """
    Gets a module's object from datastore.

    Attempts to get a module from the datastore. If it is not found, attempt 
    to retrieve details of said module from UL website and add the module to 
    the database before returning this module.

    @param module_code: Module code to get details for
    @type module_code: String

    @return An object of type Module for the module, or None if match not found
    """
    result = cls.query(cls.code == module_code).get()

    if result:
      return result

    result = course.module(module_code)

    if result == -1:
      return None

    new_module = Module(
      code = result['code'].lower(),
      name = result['name'])
    new_module.put()

    return new_module

  @classmethod
  def get_module_dict(cls, module_code):
    """
    Gets a module's details as an OrderedDict from datastore.

    Attempts to get a course from the datastore. If it is not found, attempt 
    to retrieve details of said course from UL website and add the course to 
    the database before returning this module

    @param module_code: Module code to get details for
    @type module_code: String

    @return An OrderedDict containing the module code and name, or -1 if match 
    not found
    """
    result = cls.get_module(module_code)

    if not result:
      return -1

    data = OrderedDict([
      ('kind', 'module'),
      ('code', result.code),
      ('name', result.name),
    ])

    return data

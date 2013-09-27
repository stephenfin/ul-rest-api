#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" scheduling.py: Datasources for the scheduling services """

from __future__ import print_function

from collections import OrderedDict
from google.appengine.api import memcache
from google.appengine.ext import ndb
from import_relative import import_relative
import re, os

common = import_relative('common', '..datasources')
scheduling = import_relative('scheduling', '..datasources')

class Calendar(ndb.Model):
  """ Models an academic calendar entry """
  def validate_year(self, value):
    """ Validates a year """
    if not re.match(r"20[0-9]{2}", value):
      raise ValueError
    return value

  year = ndb.StringProperty(validator=validate_year)
  autumn_start = ndb.StringProperty()
  autumn_end = ndb.StringProperty()
  spring_start = ndb.StringProperty()
  spring_end = ndb.StringProperty()
  autumn_exam_start = ndb.StringProperty()
  autumn_exam_end = ndb.StringProperty()
  spring_exam_start = ndb.StringProperty()
  spring_exam_end = ndb.StringProperty()

  @classmethod
  def get_calendar(cls, year):
    """
    Gets an academic calendar from datastore.

    Attempts to get a calendar from the datastore. If it is not found, attempt 
    to retrieve details of said calendar from UL website and add the calendar to 
    the database before returning this calendar.

    @param year: Calendar year to get details for
    @type year: String

    @return An object of type Calendar for the calendar, or None if match not 
    found
    """

    result = cls.query(cls.year == year).get()

    if result:
      return result

    result = scheduling.calendar(year)

    if result == -1:
      return None

    new_calendar = Calendar(
      year = result['items']['year'],
      autumn_start = result['items']['autumn']['start'],
      autumn_end = result['items']['autumn']['end'],
      spring_start = result['items']['spring']['start'],
      spring_end = result['items']['spring']['end'],
      autumn_exam_start = result['items']['autumn_exam']['start'],
      autumn_exam_end = result['items']['autumn_exam']['end'],
      spring_exam_start = result['items']['spring_exam']['start'],
      spring_exam_end = result['items']['spring_exam']['end'])
    new_calendar.put()

    return new_calendar

  @classmethod
  def get_calendar_dict(cls, year):
    """
    Gets a academic calendar's details as an OrderedDict from datastore.

    Attempts to get a academic calendar from the datastore. If it is not 
    found, attempt to retrieve details of said calendar from UL website and 
    add the calendar to the database before returning this calendar.

    @param year: Calendar year to get details for
    @type year: String in format xxxx, i.e. 2009

    @return An OrderedDict containing the calendar year and semester and exam 
    dates for said year, or -1 if match not found
    """
    result = cls.get_calendar(year)

    if not result:
      return -1

    data = OrderedDict([
      ('kind', 'calendar'),
      ('year', result.year),
      ('autumn', OrderedDict([
        ('start', result.autumn_start),
        ('end', result.autumn_end)
        ])),
      ('spring', OrderedDict([
        ('start', result.spring_start),
        ('end', result.spring_end)
        ])),
      ('autumn_exam', OrderedDict([
        ('start', result.autumn_exam_start),
        ('end', result.autumn_exam_end)
        ])),
      ('spring_exam', OrderedDict([
        ('start', result.spring_exam_start),
        ('end', result.spring_exam_end)
        ]))
    ])

    return data

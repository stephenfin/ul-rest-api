#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" handlers.py: Handlers for all URIs in application """

import collections
import webapp2
import json

import datasources.course as course
import datasources.geolocation as geolocation
import datasources.scheduling as scheduling
import datasources.staff as staff

from datetime import datetime

class DocumentationHandler(webapp2.RequestHandler):
  """ Documentation Services """
  def get(self):
    #Parse the URI
    self.response.write("Documentation") 

'''
Handles the following services:
  Scheduling:
    calendar            Academic Calendar
    timetable           Semester Timetables
    exam_timetable      Exam Timetables
'''
class SchedulingHandler(webapp2.RequestHandler):
  """ Scheduling Services """
  def get(self):
    #Parse the URI
    self.response.write("Scheduling") 

    #Parse the parameters from the URL
    query = self.request.get('q')

    if not query:
      self.generate_error('Please include the parameter \'q\'')
      return

    result = {
    '/api/v1/timetable' : self.get_timetable,
    '/api/v1/exam_timetable' : self.get_exam_timetable,
    '/api/v1/calendar' : self.get_calendar,
    }.get(self.request.path, self.error)(query)

    self.response.write(json.dumps(result))

  '''
  Retrieve the timetable for a given ID and return the result 
  '''
  def get_timetable(self, query):
    # Retrieve a timeable for a given ID number (query)
    data = scheduling.semester_timetable(query)
    
    if not data:
      return -1

    result = collections.OrderedDict()
    result['id'] = query
    result['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result['data'] = data

    return result

  def get_exam_timetable(self, query):
    self.response.write("Error")

  def get_calendar(self, query):
    # Retrieve a calendar for a given year (query)
    data = scheduling.calendar(query)
    
    if not data:
      return -1

    result = collections.OrderedDict()
    result['id'] = query
    result['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result['data'] = data

    return result

  def error(self, query):
    self.response.write("Error")

'''
Handles the following services:
  Geolocation:
    building            List all buildings on campus or parse a building code
    room                Parse a room code
'''
class GeolocationHandler(webapp2.RequestHandler):
  """ Geolocation Services """
  def get(self):
    #Parse the URI
    self.response.write("Geolocation") 

'''
Handles the following services:
  Course:
    course              Provides a brief overview of a course
    module              Provides a brief overview of a module
'''
class CourseHandler(webapp2.RequestHandler):
  """ Course Services """
  def get(self):
    #Parse the URI
    self.response.write("Course") 

'''
Handles the following services:
  Staff:
    staff               Provides a brief overview of a staff member
'''
class StaffHandler(webapp2.RequestHandler):
  """ Staff Services """
  def get(self):
    #Parse the URI
    self.response.write("Staff") 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" handlers.py: Handlers for all URIs in application """

from collections import OrderedDict
import webapp2
import json

import datasources.common as common
import datasources.course as course
import datasources.geolocation as geolocation
import datasources.scheduling as scheduling
import datasources.staff as staff

from datetime import datetime

class BaseHandler(webapp2.RequestHandler):
  """ Base Handler """
  def generate_response(self, data):
    """
    Generates a suitable json response to present to the end user

    @param data_type: The type of data we're returning
    @type data_type: String
    @param data: The actual data
    @param data: List
    """
    rfc3339_ts = datetime.utcnow().isoformat("T") + "Z"

    response_data = OrderedDict([
      ("api_version", common.API_VERSION),
      ("data_created", rfc3339_ts),
      ("data", data),
    ])

    response = OrderedDict()
    response['response'] = response_data

    self.response.headers['Content-Type'] = 'application/json' 
    self.response.write(json.dumps(response))

  def generate_error_response(self, error_message=None):
    """
    Generates a suitable json error response to present to the end user

    @param error_message: The error message to show to the end user
    @type data_type: String
    """
    if not error_message:
      error_message = 'Invalid parameter \'q\''

    error_data = OrderedDict([
      ("message", error_message),
    ])

    error = OrderedDict()
    error['error'] = error_data

    self.response.headers['Content-Type'] = 'application/json' 
    self.response.write(json.dumps(error))


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
class SchedulingHandler(BaseHandler):
  """ Scheduling Services """
  def get(self):
    #Parse the parameters from the URL
    query = self.request.get('q')

    if not query:
      self.generate_error_response('Please include the parameter \'q\'')
      return

    result = {
      '/api/v1/timetable' : self.get_timetable,
      '/api/v1/exam_timetable' : self.get_exam_timetable,
      '/api/v1/calendar' : self.get_calendar,
    }.get(self.request.path, self.generate_error_response)(query)

    self.generate_response(result)

  '''
  Retrieve the timetable for a given ID and return the result 
  '''
  def get_timetable(self, query):
    # Retrieve a timeable for a given ID number (query)
    data = scheduling.semester_timetable(query)
    
    if not data:
      return -1

    return data

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
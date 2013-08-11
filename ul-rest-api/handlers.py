#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" handlers.py: Handlers for all URIs in application """

from collections import OrderedDict
import json
import urllib, urllib2
import webapp2

import datasources.common as common
import datasources.course as course
import datasources.geolocation as geolocation
import datasources.scheduling as scheduling
import datasources.staff as staff

from datetime import datetime

class BaseHandler(webapp2.RequestHandler):
  """ Base Handler """
  def validate_parameters(self, additional_params):
    """
    Validates that the <q> and <key> parameters, along with any other required 
    params, are included in the request.

    @param params: A list of required params other than <q> and <key>
    @type params: List of Strings

    @return True if validation succesful, else False
    """
    #TODO: validate key

    missing_params = []

    params = ['q'] + additional_params
    for param in params:
      if not self.request.get(param):
        error = OrderedDict()
        error['error'] = 'missingParam'
        error['details'] = param
        missing_params.append(error)

    if missing_params:
      #Generate an error response
      self.generate_error_response('Missing parameters', missing_params)
      return False

    return True

  def generate_response(self, data):
    """
    Generates a suitable json response to present to the end user

    @param data: The actual data
    @param data: List
    """
    rfc3339_ts = datetime.utcnow().isoformat("T") + "Z"

    response_data = OrderedDict([
      ('api_version', common.API_VERSION),
      ('data_created', rfc3339_ts),
      ('data', data),
    ])

    response = OrderedDict()
    response['response'] = response_data

    self.response.headers['Content-Type'] = 'application/json' 
    self.response.write(json.dumps(response))

  def generate_error_response(self, error_message, errors=None):
    """
    Generates a suitable json error response to present to the end user

    @param error_message: The error message to show to the end user
    @type data_type: String
    """
    if not errors:
      error = OrderedDict()
      error['error'] = 'generalError'
      error['details'] = error_message
      errors = [error]

    error_data = OrderedDict([
      ('message', error_message),
      ('errors', errors)
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
    if not self.validate_parameters([]):
      return    #Quit, since parameters are invalid

    #Parse the parameters from the URL
    query = self.request.get('q')

    try:
      result = {
        '/api/v1/timetable' : scheduling.semester_timetable,
        '/api/v1/calendar' : scheduling.calendar,
      }.get(self.request.path)(query)

      if not result:
        self.generate_error_response('An Error Occurred')

      self.generate_response(result)
    except urllib2.URLError as ex:
      self.generate_error_response('An Error Occured Contacting the Site')
    except IOError as ex:
      self.generate_error_response('An Error Occured Contacting the Site')
    except Exception as ex:
      self.generate_error_response('An Unknown Error Occured')

'''
Handles the following services:
  Geolocation:
    building            List all buildings on campus or parse a building code
    room                Parse a room code
'''
class GeolocationHandler(BaseHandler):
  """ Geolocation Services """
  def get(self):
    if not self.validate_parameters([]):
      return    #Quit, since parameters are invalid

    #Parse the parameters from the URL
    query = self.request.get('q')

    result = {
      '/api/v1/building' : geolocation.building,
      '/api/v1/room' : geolocation.room,
    }.get(self.request.path)(query)

    if not result:
      self.generate_error_response('An Error Occurred')
      
    self.generate_response(result)  

'''
Handles the following services:
  Course:
    course              Provides a brief overview of a course
    module              Provides a brief overview of a module
'''
class CourseHandler(BaseHandler):
  """ Course Services """
  def get(self):
    if not self.validate_parameters([]):
      return    #Quit, since parameters are invalid

    #Parse the parameters from the URL
    query = self.request.get('q')

    result = {
      '/api/v1/course' : course.course,
      '/api/v1/module' : course.module,
    }.get(self.request.path)(query)

    if not result:
      self.generate_error_response('An Error Occurred')
      
    self.generate_response(result)

'''
Handles the following services:
  Staff:
    staff               Provides a brief overview of a staff member
'''
class StaffHandler(BaseHandler):
  """ Staff Services """
  def get(self):
    if not self.validate_parameters([]):
      return    #Quit, since parameters are invalid

    #Parse the parameters from the URL
    query = self.request.get('q')

    #Since name (query) should have been received in format "<first>,<last>", 
    #we need to split it into two strings
    query = query.split(',')

    result = {
      '/api/v1/staff' : staff.staff,
    }.get(self.request.path)(query[0], query[1])

    if not result:
      self.generate_error_response('An Error Occurred')
      
    self.generate_response(result)  
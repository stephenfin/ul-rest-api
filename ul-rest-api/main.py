#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" main.py: Main application file for GAE Web Application """

import handlers
import webapp2
from webapp2_extras import routes

app = webapp2.WSGIApplication([
    routes.PathPrefixRoute('/api/v1', [
      webapp2.Route('/', handlers.DocumentationHandler,
        name=""),
      webapp2.Route('/calendar', handlers.SchedulingHandler, 
        name="calendar"),
      webapp2.Route('/timetable', handlers.SchedulingHandler, 
        name="timetable"),
      webapp2.Route('/examtimetable', handlers.SchedulingHandler, 
        name="examtimetable"),
      webapp2.Route('/building', handlers.GeolocationHandler, 
        name="building"),
      webapp2.Route('/room', handlers.GeolocationHandler, 
        name="room"),
      webapp2.Route('/course', handlers.CourseHandler, 
        name="course"),
      webapp2.Route('/module', handlers.CourseHandler, 
        name="module"),
      webapp2.Route('/staff', handlers.StaffHandler, 
        name="staff"),
    ]),
], debug=True)

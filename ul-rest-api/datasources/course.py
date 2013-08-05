#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" course.py: Datasources for the course services """

from __future__ import print_function

import common
import re
import lxml.html

def course(course_code):
  """
  Retrieve and parses course information from UL site

  >>> course("LM118")
  ('LM069', ' Computer Engineering', 
    'http://www3.ul.ie/courses/ComputerEngineering.shtml')

  @param module_code: Course code to get details for
  @type module_code: String

  @return A tuple containing the original course code, title of course and web 
  address of course page, or -1 if match not found
  """
  url = 'http://www3.ul.ie/courses/AlphabeticalList.shtml'
  
  row = common.get_page(url).xpath('//p//a[contains(., \'{0}\')]'.format(course_code))

  # Handle course does not exist (either now or ever)
  if not row:
    return -1

  text_value = row[0].xpath('./text()')[0]
  link_value = row[0].xpath('./@href')[0]

  # Parse course code and name from combined string using Regex
  course_re = re.match(common.COURSE_NAME_RE, text_value)
  course_data = course_re.group('code', 'name')

  # Parse course URL from href attribute
  course_data = course_data + ('http://www3.ul.ie/courses/' + link_value,) 
  
  return course_data

def module(module_code):
  """
  Retrieve and parses module information from UL site

  >>> module("CE4702")
  ('CE4702', u'Computer Software 2')

  @param module_code: Module code to get details for
  @type module_code: String

  @return A tuple containing the original module code and title of module, or 
  -1 if match not found
  """
  url = 'http://193.1.101.55/tt_moduledetails_res.asp'
  
  params = { 
    'T1' : module_code
  }

  # Get first match based on child. Solution from:
  # http://stackoverflow.com/questions/9683054/xpath-to-select-element-based-on-childs-child-value
  rows = common.get_page(url, params).xpath('//table//table/tr')

  # no matches
  if not rows:
    return -1
  
  return (module_code, common.tidy_tag(rows[1].xpath('td[2]')[0]))

if __name__ == '__main__':
  print(module('CE4702'))
  print(module('CE4708'))
  print(module('GE4555'))
  print(course('LM069'))
  print(course('LM071'))
  print(course('LM118'))

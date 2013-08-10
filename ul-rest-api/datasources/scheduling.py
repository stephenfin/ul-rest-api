#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" scheduling.py: Datasources for the scheduling services """

from __future__ import print_function
from collections import OrderedDict

import common
import re
import lxml.html

def semester_timetable(student_id):
  """
  Retrieve and parses semester timetable from UL timetable site

  @param student_id: Student ID to get timetable for
  @type student_id: String

  @return An OrderedDict of OrderedDicts containing start and end times, 
  module code, class type and room for events, or -1 if match not found
  """
  url = 'http://www.timetable.ul.ie/tt2.asp'
  
  params = { 
    'T1' : student_id
  }

  rows = common.get_page(url, params).xpath('//div/table/tr[2]/td')

  result = []

  for idx, day in enumerate(rows):
    periods = []
    for idx2, period in enumerate(day.xpath('./p')):
      # Convert mostly unstructured text from within 'p' tag into a list of words.
      # Each word will correspond to a line on the actual timetable page.
      # Example output:
      #   [u'15:00', u'-', u'16:00', u'EE4617', u'- LEC -', u'LCO017', u'Wks:1-8,10-14']
      #   [u'17:00', u'-', u'18:00', u'CE4218', u'- LAB -', u'2A', u'B2042', u'Wks:1-8,10-14']
      data = filter(None, [x.strip() for x in common.tidy_tag(period).split('\n')])

      # Handle empty data cells
      if not data:
        continue
    
      periods.append((idx2, _parse_timetable_entry(data)))
    result.append((idx, OrderedDict(periods)))
  return OrderedDict(result)

def _parse_timetable_entry(data):
  '''
  Parses a single timetable entry

  @param data: The given timetable period's data list
  @type data: list

  @return An OrderedDict containing details for a single timetable event
  '''
  start_time = data[0]
  end_time = data[2]
  module = data[3].replace('-', '').strip()
  period_type = data[4].replace('-', '').strip()
  room = data[-2]
  weeks = data[-1]

  # Handle a corner case for LABs or TUTs that have an number, i.e. LAB-2A,
  # as seen above in example 2
  if data[-3] != data[4]:
    period_type = period_type + u'-' + data[-3].replace('-', '').strip()

  # Convert the Wks cell into useful data. Unfortunately this can only be 
  # done using regexs. 
  weeks_re = re.match(common.SEM_TIME_WKS_RE, weeks)
  weeks = weeks_re.group('p1_start', 'p1_end', 'p2_start', 'p2_end')

  data = OrderedDict([
    ('start_time', start_time),
    ('end_time', end_time),
    ('module', module),
    ('period_type', period_type),
    ('room', room),
    ('weeks', weeks),
  ])
  return data

def calendar(year):
  """
  Retrieve and parses academic calendar from UL calendar site

  @param year: Start year of calendar to retrieve ([year] - [year + 1])
  @type year: String

  @return A An OrderedDict containing events for calendar, plus corresponding 
  dates, or -1 if match not found
  """
  # Retrieve page and create parser object for table
  year_end = str(int(year) + 1)[2:]

  url = ('http://www2.ul.ie/web/WWW/Services/Academic_Calendar/{0}_-_{1}_'
    'Academic_Calendar').format(year, year_end)

  rows = common.get_page(url).xpath('//div[@class=\'rc-doc\']/table/tbody[1]')

  search_terms = [
    'Autumn Teaching Term',
    'Spring Teaching Term',
    'Autumn Examinations',
    'Examinations Spring'
  ]

  result_names = [
    ('autumn'),
    ('spring'),
    ('autumn_exam'),
    ('spring_exam'),
  ]

  results = []

  for idx, search_term in enumerate(search_terms):
    data = rows[0].xpath('./tr[./td/div/strong= \'{0}\']'.format(search_term))
    data = data[0].xpath('./td')
    start_date = common.tidy_tag(data[2])
    end_date = common.tidy_tag(data[3])
    result = OrderedDict([
      ('start', start_date),
      ('end', end_date),
    ])
    results.append((result_names[idx], result))

  return OrderedDict(results)

if __name__ == "__main__":
  print(semester_timetable("09005891"))
  print(semester_timetable("09005081"))
  print(calendar(2014))
  print(calendar(2013))
  print(calendar(2012))
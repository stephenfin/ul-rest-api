#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" scheduling.py: Datasources for the scheduling services """

from __future__ import print_function

import common
import re
import lxml.html

def semester_timetable(student_id):
  """
  Retrieve and parses semester timetable from UL timetable site

  >>> semester_timetable("09005891")
  [[
    (u'10:00', u'12:00', u'CE4208', u'LEC', u'ERB001', (u'1', u'8', u'10', u'14')), 
    (u'14:00', u'15:00', u'CE4518', u'LEC', u'B2041', (u'1', u'8', u'10', u'14')), 
    (u'15:00', u'17:00', u'CE4218', u'LEC', u'A1054', (u'1', u'8', u'10', u'14')), 
    (u'17:00', u'18:00', u'EE4617', u'LEC', u'A1054', (u'1', u'8', u'10', u'14'))
   ], [
    (u'15:00', u'16:00', u'CE4518', u'TUT-3A', u'B2041', (u'2', u'8', u'10', u'14'))
   ], [
    (u'09:30', u'12:30', u'CE4908', u'LEC', u'B2043 B2006', (u'1', u'8', u'10', u'14')), 
    (u'13:30', u'17:30', u'CE4908', u'LEC', u'B2043 B2006', (u'1', u'8', u'10', u'14'))
   ], [
    (u'15:00', u'16:00', u'EE4617', u'TUT-3A', u'B2041', (u'2', u'8', u'10', u'14')), 
    (u'16:00', u'18:00', u'CE4208', u'LAB-2A', u'B2043 B2042', (u'1', u'8', u'10', u'14'))
   ], [
    (u'13:00', u'14:00', u'CE4518', u'LEC', u'B2041', (u'1', u'8', u'10', u'14')), 
    (u'15:00', u'16:00', u'EE4617', u'LEC', u'LCO017', (u'1', u'8', u'10', u'14')), 
    (u'17:00', u'18:00', u'CE4218', u'LAB-2A', u'B2042', (u'1', u'8', u'10', u'14'))
   ], [
   ]
  ]

  @param student_id: Student ID to get timetable for
  @type student_id: String

  @return A list of lists of tuples containing start and end times, module 
    code, class type and room for event, or -1 if match not found
  """
  url = 'http://www.timetable.ul.ie/tt2.asp'
  
  params = { 
    'T1' : student_id
  }

  # Get first match based on child. Solution from:
  # http://stackoverflow.com/questions/9683054/xpath-to-select-element-based-on-childs-child-value
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
    
      periods.append(_parse_entry(data))
    result.append(periods)
  return result

def _parse_entry(data):
  '''
  Parses a single timetable entry

  @param data: The given timetable period's data list
  @type data: list
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

  return (start_time, end_time, module, period_type, room, weeks)

def calendar(year):
  """
  Retrieve and parses academic calendar from UL calendar site

  >>> calendar("2013")
  [ (u'Mon 09/09/2013', u'Fri 20/12/2013'), 
    (u'Mon 27/01/2014', u'Mon 19/05/2014'), 
    (u'Sat 07/12/2013', u'Fri 20/12/2013'), 
    (u'Tue 06/05/2014', u'Mon 19/05/2014') ]

  @param year: Start year of calendar to retrieve ([year] - [year + 1])
  @type year: String

  @return A tuple of tuples containing start and end dates for calendar, or -1 
  if match not found
  """
  # Retrieve page and create parser object for table
  year_end = str(int(year) + 1)[2:]

  url = ('http://www2.ul.ie/web/WWW/Services/Academic_Calendar/{0}_-_{1}_'
    'Academic_Calendar').format(year, year_end)

  # Get first match based on child. Solution from:
  # http://stackoverflow.com/questions/9683054/xpath-to-select-element-based-on-childs-child-value
  rows = common.get_page(url).xpath('//div[@class=\'rc-doc\']/table/tbody[1]')

  search_terms = [
    'Autumn Teaching Term',
    'Spring Teaching Term',
    'Autumn Examinations',
    'Examinations Spring'
  ]

  results = []

  for search_term in search_terms:
    data = rows[0].xpath('./tr[./td/div/strong= \'{0}\']'.format(search_term))
    data = data[0].xpath('./td')
    start_date = common.tidy_tag(data[2])
    end_date = common.tidy_tag(data[3])
    results.append((start_date, end_date))

  return results

if __name__ == "__main__":
  print(semester_timetable("09005891"))
  print(semester_timetable("09005081"))
  print(calendar(2014))
  print(calendar(2013))
  print(calendar(2012))
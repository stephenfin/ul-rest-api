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
  [(0, [
    (0, [
      ('start_time', u'10:00'), ('end_time', u'12:00'), ('module', u'Ce4208'), 
      ('period_type', u'Lec'), ('room', u'Erb001'), 
      ('weeks', (u'1', u'8', u'10', u'14'))]), 
    (1, [
      ('start_time', u'14:00'), ('end_time', u'15:00'), ('module', u'Ce4518'), 
      ('period_type', u'Lec'), ('room', u'B2041'), 
      ('weeks', (u'1', u'8', u'10', u'14'))]), 
    (2, [
      ('start_time', u'15:00'), ('end_time', u'17:00'), ('module', u'Ce4218'), 
      ('period_type', u'Lec'), ('room', u'A1054'), 
      ('weeks', (u'1', u'8', u'10', u'14'))]), 
    (3, [
      ('start_time', u'17:00'), ('end_time', u'18:00'), ('module', u'Ee4617'), 
      ('period_type', u'Lec'), ('room', u'A1054'), 
      ('weeks', (u'1', u'8', u'10', u'14'))])
  ]), (1, [
    (0, [
      ('start_time', u'15:00'), ('end_time', u'16:00'), ('module', u'Ce4518'), 
      ('period_type', u'Tut-3A'), ('room', u'B2041'), 
      ('weeks', (u'2', u'8', u'10', u'14'))])
  ]), (2, [
    (0, [
      ('start_time', u'09:30'), ('end_time', u'12:30'), ('module', u'Ce4908'), 
      ('period_type', u'Lec'), ('room', u'B2043 B2006'), 
      ('weeks', (u'1', u'8', u'10', u'14'))]), 
    (1, [
      ('start_time', u'13:30'), ('end_time', u'17:30'), ('module', u'Ce4908'), 
      ('period_type', u'Lec'), ('room', u'B2043 B2006'), 
      ('weeks', (u'1', u'8', u'10', u'14'))])
  ]), (3, [
    (0, [
      ('start_time', u'15:00'), ('end_time', u'16:00'), ('module', u'Ee4617'), 
      ('period_type', u'Tut-3A'), ('room', u'B2041'), 
      ('weeks', (u'2', u'8', u'10', u'14'))]), 
    (1, [
      ('start_time', u'16:00'), ('end_time', u'18:00'), ('module', u'Ce4208'), 
      ('period_type', u'Lab-2A'), ('room', u'B2043 B2042'), 
      ('weeks', (u'1', u'8', u'10', u'14'))])
  ]), (4, [
    (0, [
      ('start_time', u'13:00'), ('end_time', u'14:00'), ('module', u'Ce4518'), 
      ('period_type', u'Lec'), ('room', u'B2041'), 
      ('weeks', (u'1', u'8', u'10', u'14'))]), 
    (1, [
      ('start_time', u'15:00'), ('end_time', u'16:00'), ('module', u'Ee4617'), 
      ('period_type', u'Lec'), ('room', u'Lco017'), 
      ('weeks', (u'1', u'8', u'10', u'14'))]), 
    (2, [
      ('start_time', u'17:00'), ('end_time', u'18:00'), ('module', u'Ce4218'), 
      ('period_type', u'Lab-2A'), ('room', u'B2042'), 
      ('weeks', (u'1', u'8', u'10', u'14'))])
  ]), (5, [
  ])]

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
    
      periods.append((idx2, _parse_timetable_entry(data)))
    result.append((idx, periods))
  return result

def _parse_timetable_entry(data):
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

  data = [
    ('start_time', start_time),
    ('end_time', end_time),
    ('module', module),
    ('period_type', period_type),
    ('room', room),
    ('weeks', weeks),
  ]
  return data

def calendar(year):
  """
  Retrieve and parses academic calendar from UL calendar site

  >>> calendar("2013")
  [('autumn', [
    ('start', u'Mon 09/09/2013'), ('end', u'Fri 20/12/2013')
  ]), ('spring', [
    ('start', u'Mon 27/01/2014'), ('end', u'Mon 19/05/2014')
  ]), ('autumn_exam', [
    ('start', u'Sat 07/12/2013'), ('end', u'Fri 20/12/2013')
  ]), ('spring_exam', [
    ('start', u'Tue 06/05/2014'), ('end', u'Mon 19/05/2014')
  ])]

  @param year: Start year of calendar to retrieve ([year] - [year + 1])
  @type year: String

  @return A list of events for calendar, plus corresponding dates, or -1 if
  match not found
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
    result = [
      ('start', start_date),
      ('end', end_date),
    ]
    results.append((result_names[idx], result))

  return results

if __name__ == "__main__":
  print(semester_timetable("09005891"))
  print(semester_timetable("09005081"))
  print(calendar(2014))
  print(calendar(2013))
  print(calendar(2012))
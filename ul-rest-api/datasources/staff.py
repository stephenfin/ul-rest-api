#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" staff.py: Datasources for staff services """

from __future__ import print_function
from collections import OrderedDict

import common
import lxml.html

def staff(first_name, last_name):
  """
  Search UL Staff Directory for a given name (first and last)

  @param first_name: The first name of staff member to search for
  @type first_name: String
  @param last_name: The last name of staff member to search for
  @type last_name: String

  @return An OrderedDict containing the name, department, office and phone of 
  given person, or -1 if match not found.
  """
  # Retrieve page and create parser object for table
  url = 'http://www.ul.ie/staff-search'

  params = {
  'keyword' : first_name.lower(),
  'filter' : 'givenname'
  }

  rows = common.get_page(url, params).xpath('//p[@class=\'result clearfix\']')

  # no matches
  if len(rows) < 1:
    return -1
  
  # single match
  if len(rows) == 1:
    return _parse_entry(rows[0])
  
  # multiple matches  
  for idx, row in enumerate(rows):
    # match on last name also
    result = _parse_staff_entry(row, last_name)
    if result:
      return result

  return -1

def _parse_staff_entry(row, last_name):
  """
  Parses a single staff entry

  @param row: The given staff member's lxml HtmlElement row
  @type row: lxml.html.HtmlElement

  @return An OrderedDict containing the name, department, office and phone of 
  given person if last name matches, or null if match not found.
  """
  name = row.xpath('span[@class=\'name\']/text()')[0]

  if not name.split()[1].lower() == last_name.lower():
    return

  dept = row.xpath('span[@class=\'department\']/text()')
  room = row.xpath('span[@class=\'office\']/text()')[0]
  tel = row.xpath('span[@class=\'phone\']/text()')

  if dept:
    dept = dept[0]

  if tel:
    tel = tel[0]

  data = OrderedDict([
    ('name', name),
    ('dept', dept),
    ('room', room),
    ('tel', tel),
  ])

  return data

if __name__ == '__main__':
  print(staff(first_name = 'John', last_name = 'Nelson'))
  print(staff(first_name = 'Natalia', last_name = 'Kopteva'))
  print(staff(first_name = 'Ciaran', last_name = 'MacNamee'))
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" geolocation.py: Datasources for the geolocation services """

from __future__ import print_function
from collections import OrderedDict

import common
import re
import lxml.html

def building(building_name):
  """
  Retrieve and parses building information from UL site

  @param module_code: Buidling name to get details for
  @type module_code: String

  @return An OrderedDict containing the building name, a thumbnail and web 
  address of building information page, or -1 if match not found
  """
  url = 'https://www2.ul.ie/web/WWW/Services/Buildings_and_Estates/At_A_Glance/'
  
  row = common.get_page(url).xpath('//div[@class=\'rc-doc\']/table/tbody[1]/tr\
    [contains(.//strong, \'{0}\')]'.format(building_name.title()))

  # Handle building does not exist
  if not row:
    return -1

  building_data = row[0].xpath('./td[1]/strong/text()')[0]
  building_image = 'https://www2.ul.ie' + row[0].xpath('./td[2]/a/img/@src')[0]
  building_link = 'https://www2.ul.ie' + row[0].xpath('./td[2]/a/@href')[0]

  data = OrderedDict([
    ('kind', 'building'),
    ('name', building_data),
    ('thumb', building_image),
    ('url', building_link),
  ])
  
  return data

def room(room_code):
  """
  Parses a room code using lookups of hardcoded dictionaries

  @param room_code: Room code to get details for
  @type room_code: String

  @return An OrderedDict containing the room code, building name, building 
  code, floor and room number, or -1 if match not found
  """

  # Token maps for building. Hardcoded here as currently no readily available
  # online source for this data. Data originally sourced from here:
  # http://www2.ul.ie/web/WWW/Services/Student_Affairs/Student_Administration
  #   /Admissions/New_Student_Guide/Numbering_System_for_Rooms
  one_char_token_map = {
    'A':'Main Building', 
    'B':'Main Building', 
    'C':'Main Building',
    'D':'Main Building', 
    'E':'Main Building',
    'F':'Foundation Building',
    'L':'Lonsdale', 
    'P':'PE Building', 
    'S':'Schuman Building', 
  }

  two_char_token_map = {
    'GL':'Glucksman Library', 
    'CS':'Computer Science Building', 
    'UA':'University Arena', 
    'MS':'Materials and Surface Science Institute',
    'MS':'Millstream Courtyard Building', 
    'ER':'Engineering Research Building',
    'LC':'Languages Building', 
    'KB':'Kemmy Business School', 
    'HS':'Health Sciences Building',
    'SH':'Schrodinger Building',
  }

  # Clean up room code, removing any dashes or extraneous spaces
  room_code = str(room_code.upper().replace('-','').strip())

  # Two digit building code
  if (room_code[0:2] in two_char_token_map):
    building_code = room_code[0:2]
    building_name = two_char_token_map[building_code]
    floor_code = room_code[2]
    room_number = room_code[3:]
  # One digit building code
  elif (room_code[0] in one_char_token_map):
    building_code = room_code[0]
    building_name = one_char_token_map[building_code]
    floor_code = room_code[1]
    room_number = room_code[2:]
  # No match found
  else:
    return -1

  data = OrderedDict([
    ('kind', 'room'),
    ('room_code', room_code),
    ('building_name', building_code),
    ('building_code', building_name),
    ('floor', floor_code),
    ('room', room_number),
  ])
  return data

if __name__ == '__main__':
  print(building('Schuman'))
  print(building('Main'))
  print(building('Engineering Research'))
  print(room('ER2-081'))
  print(room('C2-061'))
  print(room('LCG056'))
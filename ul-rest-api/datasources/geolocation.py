#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" geolocation.py: Datasources for the geolocation services """

from __future__ import print_function

import common
import re
import lxml.html

def building(building_name):
  """
  Retrieve and parses course information from UL site

  >>> building("Schrodinger")
  ('sh', 'Schrodinger', '')

  @param module_code: Buidling code or name to get details for
  @type module_code: String

  @return A tuple containing the building code, building name and web 
  address of building image, or -1 if match not found
  """
  url = 'https://www2.ul.ie/web/WWW/Services/Buildings_and_Estates/At_A_Glance/'
  
  '''
  row = common.get_page(url).xpath('//div[@class=\'rc-doc\']/table/tbody[1]\
    //strong[contains(., \'{0}\')]'.format(building_name.title()))
  '''
  row = common.get_page(url).xpath('//div[@class=\'rc-doc\']/table/tbody[1]/tr\
    [contains(.//strong, \'{0}\')]'.format(building_name.title()))

  # Handle building does not exist
  if not row:
    return -1

  building_data = (row[0].xpath('./td[1]/strong/text()')[0], )
  building_image = 'https://www2.ul.ie' + row[0].xpath('./td[2]/a/img/@src')[0]
  building_link = 'https://www2.ul.ie' + row[0].xpath('./td[2]/a/@href')[0]

  # Parse course URL from href attribute
  building_data = (building_data, building_image, building_link) 
  
  return building_data

def room(room_code):
  """
  Retrieve and parses course information from UL site

  >>> building("Schrodinger")
  ('sh', 'Schrodinger', '')

  @param module_code: Buidling code or name to get details for
  @type module_code: String

  @return A tuple containing the building code, building name and web 
  address of building image, or -1 if match not found
  """

  # Token maps for building. Hardcoded here as currently no readily available
  # online source for this data. Data sourced from here:
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
  }

  # Clean up room code, removing any dashes or extraneous spaces
  room_code = str(room_code.upper().replace('-','').strip())

  # Two digit building code
  if (room_code[0:2] in two_char_token_map):
    building_code = room_code[0:2]
    building_name = two_char_token_map[building_code]
    floor_code = room_code[2]
    room_number = room_code[3:]
    return (building_code, building_name, floor_code, room_number)

  # One digit building code
  if (room_code[0] in one_char_token_map):
    building_code = room_code[0]
    building_name = one_char_token_map[building_code]
    floor_code = room_code[1]
    room_number = room_code[2:]
    return (building_code, building_name, floor_code, room_number)

  # Match not found
  return -1

if __name__ == '__main__':
  print(building('Schuman'))
  print(building('Main'))
  print(building('Engineering Research'))
  print(room('ER2-081'))
  print(room('C2-061'))
  print(room('LCG056'))
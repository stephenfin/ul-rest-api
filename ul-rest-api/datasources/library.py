#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

from __future__ import print_function
from collections import OrderedDict

import requests
import lxml.html

base_url = 'https://capitadiscovery.co.uk/ul/'

def login(student_id):
  """
  Ensures that a user has been validated (i.e. logged in). 

  Checks title of page returned after attempted login for "log in" substring, 
  as failure during login will generate a page containing the string "Log in 
  to My Library Account"

  @param response: The response from the login request
  @type response: requests.models.Response

  @return session if authenticated, else None
  """

  url = 'https://capitadiscovery.co.uk/ul/sessions'

  # Website requires IDs beginning with 0 to prepended with another 0
  if student_id[0] == '0':
    student_id = '0' + student_id

  params = {
    'barcode' : student_id,
  } 

  with requests.session() as s: 
    s.post(url, data=params)

    if validate_login(s):
      return s
    else:
      return None

def validate_login(session):
  """
  Ensures that a user has been validated (i.e. logged in). 

  Checks title of page returned after attempted login for "log in" substring, 
  as failure during login will generate a page containing the string "Log in 
  to My Library Account"

  @param response: The response from the login request
  @type response: requests.models.Response

  @return True if authenticated, else False
  """

  url = 'https://capitadiscovery.co.uk/ul/account'

  response = session.get(url)
  doc = lxml.html.document_fromstring(response.content)
  doc = doc.xpath('/html/body/div/div[2]/div[4]/h1/text()')

  if not doc or 'log in' in doc[0].lower():
    return False
  
  return True

def loans(student_id):
  """
  Retrieve a list of loans for a given student

  @param student_id: Student ID to get loans for
  @type student_id: String

  @return An OrderedDict containing loans for student
  """

  url = 'https://capitadiscovery.co.uk/ul/account'

  session = login(student_id)

  if session is None:
    return

  doc = session.get(url)

  return doc

def charges(student_id):
  """
  Retrieve a list of charges for a given student

  @param student_id: Student ID to get charges for
  @type student_id: String

  @return An OrderedDict containing charges for student
  """
  
  url = 'https://capitadiscovery.co.uk/ul/account/charges'

  session = login(student_id)

  if session is None:
    return

  doc = session.get(url)
  doc = lxml.html.document_fromstring(doc.content)
  doc = doc.xpath('//table[@id=\'accountDetails\']/tbody/tr')

  if doc is None:
    return

  loans = []

  for row in doc:
    loan = OrderedDict([
      ('date', row.xpath('td[1]/text()')[0]),
      ('type', row.xpath('td[2]/text()')[0]),
      ('amount', row.xpath('td[3]/text()')[0]),
      ('details', row.xpath('td[4]/text()')[0]),
    ])
    loans.append(loan)

  return loans

def reservations(student_id):
  """
  Retrieve a list of reservations for a given student

  @param student_id: Student ID to get reservations for
  @type student_id: String

  @return An OrderedDict containing reservations for student
  """

  url = 'https://capitadiscovery.co.uk/ul/account/reservations'
  
  pass

def bookings(student_id):
  """
  Retrieve a list of bookings for a given student

  @param student_id: Student ID to get bookings for
  @type student_id: String

  @return An OrderedDict containing bookings for student
  """

  url = 'https://capitadiscovery.co.uk/ul/account/bookings'

  pass

def history(student_id):
  """
  Retrieve a list of previous loans for a given student

  @param student_id: Student ID to get previous loans for
  @type student_id: String

  @return An OrderedDict containing previous loans for student
  """

  url = 'https://capitadiscovery.co.uk/ul/account/history'

  session = login(student_id)

  if session is None:
    return

  doc = session.get(url)
  doc = lxml.html.document_fromstring(doc.content)
  doc = doc.xpath('//table[@id=\'history\']/tbody/tr')

  if doc is None:
    return

  loans = []

  for row in doc:
    loan = OrderedDict([
      ('title', row.xpath('th[1]/text()')[0]),
      ('thumb', base_url + row.xpath('th[1]/a/img/@src')[0]),
      ('link', base_url + row.xpath('th[1]/a/@href')[0]),
      ('borrowed', row.xpath('td[1]/text()')[0]),
      ('returned', row.xpath('td[2]/text()')[0]),
    ])
    loans.append(loan)

  return loans

if __name__ == '__main__':
  print(charges('09005891'))
  print(history('09005891'))
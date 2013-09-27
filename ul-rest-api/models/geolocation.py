#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" geolocation.py: Datasources for the geolocation services """

from __future__ import print_function

from collections import OrderedDict
from google.appengine.api import memcache
from google.appengine.ext import ndb
from import_relative import import_relative
import os

common = import_relative('common', '..datasources')
geolocation = import_relative('geolocation', '..datasources')

class Building(ndb.Model):
  """ Models a building entry """
  def validate_name(self, value):
    """ Validates a building name """
    # currently no way to validate this
    return value

  name = ndb.StringProperty(validator=validate_name)
  thumb = ndb.StringProperty()
  url = ndb.StringProperty()

  @classmethod
  def get_building(cls, building_name):
    """
    Gets a building's object from datastore.

    Attempts to get a building from the datastore. If it is not found, attempt 
    to retrieve details of said building from UL website and add the building to 
    the database before returning this building.

    @param building_name: Building name to get details for
    @type building_name: String

    @return An object of type Building for the building, or None if match not 
    found
    """
    result = cls.query(cls.name == building_name).get()

    if result:
      return result

    result = geolocation.building(building_name)

    if result == -1:
      return None

    new_building = Building(
      name = result['name'],
      thumb = result['thumb'],
      url = result['url'])
    new_building.put()

    return new_building

  @classmethod
  def get_building_dict(cls, building_name):
    """
    Gets a building's details as an OrderedDict from datastore.

    Attempts to get a building from the datastore. If it is not found, attempt 
    to retrieve details of said building from UL website and add the building to 
    the database before returning this building.

    @param course_code: Building name to get details for
    @type course_code: String

    @return An OrderedDict containing the building name, thumbnail url and 
    url, or -1 if match not found
    """
    result = cls.get_building(building_name)

    if not result:
      return -1

    data = OrderedDict([
      ('kind', 'building'),
      ('name', result.name),
      ('thumb', result.thumb),
      ('url', result.url),
    ])

    return data

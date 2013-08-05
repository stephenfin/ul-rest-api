# Service: calendar #

## Overview ##
This service is intended to provide access to the academic calendar for any 
given semester that data is available for.

### Source ###
[Academic Calendar Website][cr_src]

[cr_src]: http://www2.ul.ie/web/WWW/Services/Academic_Calendar "UL Academic Calendar Website"

### Approach ###
Webscraping

### Data Update Frequency ###
On each request

## Params ##

Item    | Required  | Details
:------:|:---------:|----------------------------------------------------------
key     | Required  | Your API Key
output  | Optional  | Output format. Omit this parameter to default to JSON <br> **Valid Values** : `xml, json`
q       | Required  | The starting academic calendar to retrieve the timetable for. Omit this parameter to default to current academic year <br> **Example Values** : `2012`

## Request Examples ##

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=youryear
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=youryear&output=xml
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=youryear&output=json
~~~~~~~~~~~~~

## Sample Outputs ##
### JSON ###

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=youryear
~~~~~~~~~~~~~

~~~~~~~~~~~~~{.json}
response : {
  meta : {
    created: '12-07-2013 18:09:06+00:00',
    version: '1'
  },
  data : {
    0: {
    ...
    }
  }
}
~~~~~~~~~~~~~
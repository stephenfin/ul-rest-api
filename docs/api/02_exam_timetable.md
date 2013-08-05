# Service: exam_timetable #

## Overview ##
This service is intended to provide access to exam timetables for the latest 
semester that data is available for.

### Source ###
[Timetable Website][tt_src]

[tt_src]: http://timetable.ul.ie/ "UL Timetable Website"

### Approach ###
Webscraping

### Data Update Frequency ###
On each request

## Params ##

Item    | Required  | Details
:------:|:---------:|----------------------------------------------------------
key     | Required  | Your API Key
output  | Optional  | Output format. Omit this parameter to default to JSON <br> **Valid Values** : `xml, json`
q       | Required  | The id number of the student to retrieve the timetable for <br> **Example Values** : `09009999`

## Request Examples ##

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/exam_timetable?key=yourkey&q=yourid
GET http://ul-api.stephenfinucane.com/public/v1/exam_timetable?key=yourkey&q=yourid&output=xml
GET http://ul-api.stephenfinucane.com/public/v1/exam_timetable?key=yourkey&q=yourid&output=json
~~~~~~~~~~~~~

## Sample Outputs ##
### JSON ###

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/exam_timetable?key=yourkey&q=yourid
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
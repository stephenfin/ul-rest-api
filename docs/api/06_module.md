# Service: module #

## Overview ##
This service is intended to provide a brief overview of a module, including 
information such as pre-requisites

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
q       | Required  | The module code to retrieve information for. <br> **Example Values** : `ce4701, ee4617`

## Request Examples ##

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=lm069
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=lm069&output=xml
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=lm069&output=json
~~~~~~~~~~~~~

## Sample Outputs ##
### JSON ###

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=lm069
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
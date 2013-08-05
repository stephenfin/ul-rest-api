# Service: room #

## Overview ##
This service is intended to provide information on a room

### Source ###
N/A

### Approach ###
Calculation

### Data Update Frequency ###
On each request

## Params ##

Item 	| Required? | Details
--------|-----------|----------------------------------------------------------
key 	| Required 	| Your API Key
output 	| Optional	| Output format. Omit this parameter to default to JSON <br> **Valid Values** : `xml, json`
q		| Required	| Room code to retrieve information for. <br> **Example Values** : `s, schumann`

## Request Examples ##

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/room?key=yourkey&q=c2-061
GET http://ul-api.stephenfinucane.com/public/v1/room?key=yourkey&q=c2-061&output=xml
GET http://ul-api.stephenfinucane.com/public/v1/room?key=yourkey&q=c2-061&output=json
~~~~~~~~~~~~~

## Sample Outputs ##
### JSON ###

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=c2-061
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
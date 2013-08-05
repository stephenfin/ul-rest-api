# Service: building #

## Overview ##
This service is intended to provide information on one or multiple buildings on 
campus

### Source ###
N/A

### Approach ###
Calculation

### Data Update Frequency ###
On each request

## Params ##

Item 	| Required 	| Details
:------:|:---------:|----------------------------------------------------------
key 	| Required 	| Your API Key
output 	| Optional	| Output format. Omit this parameter to default to JSON <br> **Valid Values** : `xml, json`
q		| Required	| Building code or name to retrieve information for. Omit this parameter to retrieve list of all buildings. <br> **Example Values** : `s, schumann`

## Request Examples ##

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/building?key=yourkey&q=s
GET http://ul-api.stephenfinucane.com/public/v1/building?key=yourkey&q=schumann
GET http://ul-api.stephenfinucane.com/public/v1/building?key=yourkey&q=schumann&output=xml
GET http://ul-api.stephenfinucane.com/public/v1/building?key=yourkey&q=schumann&output=json
~~~~~~~~~~~~~

## Sample Outputs ##
### JSON ###

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/calendar?key=yourkey&q=schumann
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
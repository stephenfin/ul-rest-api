# Service: staff #

## Overview ##
This service is intended to provide access to staff details for all staff that
 data is available for.

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
q       | Required  | The staff email or first and last name. <br> **Example Values** : `john.doe, JOHN_DOE`

## Request Examples ##

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/staff?key=yourkey&q=john.doe@ul.ie
GET http://ul-api.stephenfinucane.com/public/v1/staff?key=yourkey&q=JOHN_DOE
GET http://ul-api.stephenfinucane.com/public/v1/staff?key=yourkey&q=JOHN_DOE&output=xml
GET http://ul-api.stephenfinucane.com/public/v1/staff?key=yourkey&q=JOHN_DOE&output=json
~~~~~~~~~~~~~

## Sample Outputs ##
### JSON ###

~~~~~~~~~~~~~
GET http://ul-api.stephenfinucane.com/public/v1/staff?key=yourkey&q=john.doe@ul.ie
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
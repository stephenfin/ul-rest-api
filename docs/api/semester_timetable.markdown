# Service: semester_timetable #

## Overview ##
This service is intended to provide access to academic timetables for the latest semester data is available for.

### Source ###
Timetable Website

### Approach ###
Webscraping

### Data Update Frequency ###
On each request

## Params ##

<table>
  <tr>
    <td class="title">
      ** key **
    </td>
    <td class="requirement">
      Required
    </td>
    <td class="description">
      Your API Key
    </td>
  </tr>
  <tr>
    <td class="title">
      ** output **
    </td>
    <td class="requirement">
      Optional. Defaults to JSON
    </td>
    <td class="description">
      The output format (XML or JSON)
    </td>
  </tr>
  <tr>
    <td class="title">
      ** id **
    </td>
    <td class="requirement">
      Required.
    </td>
    <td class="description">
      The id number of the student to retrieve the timetable for.
    </td>
  </tr>
</table>

## Request Examples ##

>>  GET http://ul-api.stephenfinucane.com/public/v1/semester_timetable?key=yourkey&id=yourid
>>  GET http://ul-api.stephenfinucane.com/public/v1/semester_timetable?key=yourkey&id=yourid&output=xml
>>  GET http://ul-api.stephenfinucane.com/public/v1/semester_timetable?key=yourkey&id=yourid&output=json

## Sample Outputs ##
### JSON ###
>>  GET http://ul-api.stephenfinucane.com/public/v1/semester_timetable?key=yourkey&id=yourid

>>  response : {
>>    meta : {
>>      created: '12-07-2013 18:09:06+00:00',
>>      version: '1'
>>    },
>>    data : {
>>      0: {
>>        ...
>>      }
>>    }
>>  }
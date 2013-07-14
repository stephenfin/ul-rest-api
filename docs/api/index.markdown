# University of Limerick (Unofficial) Open Data API Documentation #

## Overview ##
The University of Limerick Open Data API is designed to allow anyone to access 
publicly accessible data provided by the University of Limerick from one 
convenient place. It was designed to fill a void left by the poorly integrated 
web services available within the University. It is intended to be used by 3rd 
parties in their own applications and as they see fit (note: authentication is 
required - see below)

## Acknowledgements ## 
This design of this application is based on two existing APIs. The first of 
these is the University of Waterloo Open Data API available [here][uw_src]. 
The other API is the now-depreciated Twitter 1.0 API avialable [here][tw_src]

  [uw_src]: http://api.uwaterloo.ca/ "University of Waterloo Open Data API"
  [tw_src]: https://dev.twitter.com/docs/api/1 "Twitter REST API v1 Resources"

## Design Notes ##
This API has been developed through a combination of [Python][py_src] and 
[Google App Engine][ga_src]. This allowed for ease of development and quick 
turnaround. Documentation was written in [markdown][md_src]. A number of Python
 libraries were used, including (but not limited to) lxml and epydoc.

  [py_src]: http://www.python.org/ "Python"
  [ga_src]: https://appengine.google.com/‎ "Google App Engine"
  [md_src]: http://daringfireball.net/projects/markdown "Markdown"

## Features ##
The API provides a number of features. These are listed below:
### Scheduling Services ###
  * semester_timetable  Provides access to academic timetables for the latest 
        semester data is available for
  * exam_timetable      Provides access to exam timetables for the latest 
        semester data is available for (subject to availability)
  * calendar            Provides information on the academic calendar for the 
        present year and any other years where the calendar has been scheduled
### Staff Services ###
  * staff               Provides information on staff, including room codes and
       contact information
### Course Services ####
  * course              Provides a brief overview of a course, including 
      information such as modules and requirements
  * module              Provides a brief overview of a module, including 
      information such as pre-requisites
### Geolocation Services ####
  * building            Provides information on one or multiple buildings on 
        campus
  * room                Provides informaiton on a room

## Accessing the API ##
The API is designed to function like the Twitter API. To this end, all calls 
are made to the following URL along with any required or optional parameters 
for a given service
>> http://ul-api.stephenfinucane.com/public/v1
An example call and response is given below:

### Call ###
>>  GET http://ul-api.stephenfinucane.com/public/v1/room?q=c2-061&output=json

### JSON Response ###
>>  response : {
>>    meta : {
>>      created: '12-07-2013 18:09:06+00:00',
>>      version: '1'
>>    },
>>    data : {
>>      result: {
>>        code: 'C2-061',
>>        building: 'Main Building',
>>        floor: '2',
>>        number: '061',
>>        name: ''
>>      }
>>    }
>>  }

## Restrictions on Usage ##
Due to the cost of bandwidth, it is necessary to impose a limit of 5000 calls 
on API usage. This number will likely increase in the future. However if your 
application requires more requests please contact me and I will do my best to 
accomodate you.

## Frequently Asked Questions ##
Source code for the entire project is available on [GitHub](https://github.com/stephenfin/ul-rest-api ul-rest-api). Information on contributing, submitting bug reports, downloading the source code and most other questions is available there.

## Contact ##
To submit any inquiries or suggestions (such as additional services), please contact me at:
(mailto:ul-api@stephenfinucane.com)
Alternatively, contact me through GitHub as above.
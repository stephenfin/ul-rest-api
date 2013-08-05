import webapp2
import json

from datetime import datetime

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

'''
Handles the following services:
	Scheduling:
		academic_calendar	Academic Calendar
		exam_timetable 		Exam Timetables
		semester_timetable	Semester Timetables
	Geolocation:
		building			List all buildings on campus or parse a building code
		room				Parse a room code
	Course:
		course 				Provides a brief overview of a course
		module 				Provides a brief overview of a module
	Staff:
		staff 				Provides a brief overview of a staff member
'''

class RestHandler(webapp2.RequestHandler):
	
	""" Main methods """

	def get(self):
		#Parse the parameters from the URL
		service_id = self.request.get('service')

		if not service_id:
			self.error(404)
			return

		services = {
			'academic_calendar' : self.academic_calendar,
			'exam_timetable' : self.exam_timetable,
			'timetable' : self.semester_timetable,
			'building' : self.building_search,
			'room' : self.room_search,
			'course' : self.course_search,
			'module' : self.module_search,
			'staff' : self.staff_search
		}

		services.get(service_id,self.generate_error)()

	def generate_error(self, errors = 'Required parameters invalid'):
		response = { 
			'errors' : errors
		}
		self.response.write(json.dumps(response))

	def generate_output(self, message):
		header = {
			'date_created' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		response = dict(header.items() + message.items())
		self.response.write(json.dumps(response))


	""" Scheduling Services """

	'''
	List details of a given academic calendar. Alternatively, list details of 
	current academic calendar
	'''
	def academic_calendar(self):
		#Parse the parameters from the URL
		calendar_year = self.request.get('q')

		# TODO: return all calendar details

		message = {
			'results' : 'Hello World from academic calendar service'
		}
		self.generate_output(message)

	'''
	List details of a given student's exam timetable for the current semester
	'''
	def exam_timetable(self):
		#Parse the parameters from the URL
		student_id = self.request.get('q')

		if not student_id:
			self.generate_error('Please include the parameter "q"')
			return

		# TODO: retrieve the timetable

		message = {
			'query' : student_id,
			'timetable' : 'Hello World from exam timetable service'
		}
		self.generate_output(message)

	'''
	List details of a given student's class timetable for the current semester
	'''
	def semester_timetable(self):
		#Parse the parameters from the URL
		student_id = self.request.get('q')

		if not student_id:
			self.generate_error('Please include the parameter \'q\'')
			return

		# TODO: retrieve the timetable

		message = {
			'query' : student_id,
			'timetable' : 'Hello World from semester timetable service'
		}
		self.generate_output(message)


	""" Geo-location Services """

	'''
	List details of a given building. Alternatively, list all buildings on 
	campus.
	'''
	def building_search(self):
		#Parse the parameters from the URL
		building_code = self.request.get('q')

		if not building_code:
			pass # TODO: return all buildings on campus
		else:
			pass # TODO: parse and retrieve details for the given room code

		message = {
			'query' : building_code,
			'results' : 'Hello World from building search service'
		}
		self.generate_output(message)

	'''
	Provide details for a room (i.e. parse room code)
	'''
	def room_search(self):
		#Parse the parameters from the URL
		room_code = self.request.get('q')

		if not room_code:
			self.generate_error('Please include the parameter \'q\'')
			return

		# TODO: parse and retrieve details for the given room code

		message = {
			'query' : room_code,
			'results' : 'Hello World from room search service'
		}
		self.generate_output(message)


	""" Course Services """

	'''
	List details of a given course.
	'''
	def course_search(self):
		#Parse the parameters from the URL
		course_code = self.request.get('q')

		if not course_code:
			self.generate_error('Please include the parameter \'q\'')
			return

		# TODO: parse and retrieve details for the given course code

		message = {
			'query' : course_code,
			'results' : 'Hello World from course code service'
		}
		self.generate_output(message)

	'''
	List details of a given module.
	'''
	def module_search(self):
		#Parse the parameters from the URL
		module_code = self.request.get('q')

		if not module_code:
			self.generate_error('Please include the parameter \'q\'')
			return

		# TODO: parse and retrieve details for the given module code

		message = {
			'query' : module_code,
			'results' : 'Hello World from module code service'
		}
		self.generate_output(message)


	""" Staff Services """

	'''
	List details of a given staff member. Alternatively, list all staff members matching the given criteria.

	For people search, use the following links:
		Maths & Stats: 		http://www.macsi.ul.ie/people.php
		ECE: 				http://www.ece.ul.ie/index.php/contacts/academic.html
		KBS: 				http://www.ul.ie/business/about/kbs-staff
		Physics and Energy: http://www.energy.ul.ie/people/faculty
		...etc...

	'''
	def staff_search(self):
		#Parse the parameters from the URL
		search_term = self.request.get('q')

		if not search_term:
			self.generate_error('Please include the parameter \'q\'')
			return

		# TODO: parse and retrieve details for the given room code

		message = {
			'query' : room_code,
			'results' : 'Hello World from staff search service'
		}
		self.generate_output(message)
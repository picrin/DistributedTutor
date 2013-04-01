import cgi
import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

problems_DB = db.Key.from_path('Problem','activeProblems')

def file_path(relative):
	return os.path.join(os.path.dirname(__file__), relative)
	
class MainLayout(webapp2.RequestHandler):
	"""A set of methods to present a user with their personalised layout
	"""
	def top_panel(self):
		user = User("Iva Babukova", "CS1P", "BO L1 5-05") #TODO pull a user from a database
		template_values = {"nickname": str(user.nickname),
		                   "class": str(user.klasa),
		                   "location": str(user.location),
		                   "active": user.is_problem_active()
		                   }
		path = file_path("topPanel.html")
		rendered = template.render(path, template_values)
		return rendered
	def left_panel(self):
		path = file_path("problem.html")
		return template.render(path, {})
	def right_panel(self):
		problems = db.GqlQuery("SELECT * "
		                       "FROM Problem "
		                       "WHERE ANCESTOR IS :1 "
		                       "ORDER BY date DESC LIMIT 10",
		                       problems_DB)
		problems = [problem for problem in problems]
		print "problems_table:", problems
		template_values = {"problems": problems}
		path = file_path("table.html")
		return template.render(path, template_values)
	def get(self):
		template_values = {"top_panel": self.top_panel(),
		                   "problem": self.left_panel(),
		                   "problem_table": self.right_panel()
		                   }
		path = file_path("layout.html")
		return self.response.out.write(template.render(path, template_values))

class Problem(db.Model):
	username = db.StringProperty() # nickname of the problem author
	description = db.StringProperty(multiline=True)
	hashtags = db.StringProperty(multiline=True)
	klasa = db.StringProperty()
	location = db.StringProperty()
	problem = db.BooleanProperty()
	status = db.StringProperty(choices=set(["unsolved", "picked", "solved"])) #TODO allow only: "active", "picked" and "solved"
	picked_by = db.StringProperty() #TODO point to a user
	date = db.DateTimeProperty(auto_now_add=True)
	def __str__(self):
		return "problem by user: " + str(self.username)
class User(db.Model):
	self.nickname = db.StringProperty()
	self.klasa = db.StringProperty()
	self.location = db.StringProperty()
	self.problem = db.
class ActivateProblem(webapp2.RequestHandler):
	def post(self):
		username = self.request.get('username')
		description = self.request.get('content')
		problem = Problem(parent = problems_DB)
		problem.username = username
		problem.description = description
		print "activatedProblem: ", problem
		problem.put()
		self.redirect("/")

class User(object):
	def __init__(self, nickname, klasa, location):
		self.nickname = nickname
		self.klasa = klasa
		self.location = location
		self.problem = None
	def is_problem_active(self):
		if self.problem is None:
			return "inactive"
		else:
			return "active"

app = webapp2.WSGIApplication([('/', MainLayout),
                               ('/activate_problem', ActivateProblem),
                               ], debug=True)


import cgi
import webapp2
import os
from google.appengine.ext.webapp import template

class MainLayout(webapp2.RequestHandler):
	"""Set of Methods to present a user with their personalised layout
	"""
	def top_panel(self):
		user = User("Iva Babukova", "CS1P", "BO L1 5-05")
		template_values = {"nickname": str(user.nickname),
						   "class": str(user.klasa),
						   "location": str(user.location),
						   "active": user.is_problem_active()}
		path = os.path.join(os.path.dirname(__file__), "topPanel.html")
		rendered = template.render(path, template_values)
		print rendered
		return rendered
	def get(self):
		
		template_values = {"top_panel": self.top_panel()}
		path = os.path.join(os.path.dirname(__file__), "layout.html")
		return self.response.out.write(template.render(path, template_values))


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
app = webapp2.WSGIApplication([('/', MainLayout)], debug=True)


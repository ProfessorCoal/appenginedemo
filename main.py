#
# Insightly - Google App Engine Sample Code
# Brian McConnell <brian@insight.ly>
#
# This sample code for shows how to build webapp2 compatible apps that integrate with Insightly.
# This will run as-is on Google App Engine for Python, and should also run on any webapp2
# runtime environment, although you will need to replace the App Engine django templating tools
# with the Django installation. 
#
# With the Python SDK you can access all of the major object types in Insightly, including:
#
# * Contacts
# * Emails
# * Opportunities
# * Organizations
# * Projects
# * Tasks
#
# This demo application includes a Bootstrap based sample website that enables prospective
# customers to fill out a web form, which then imports this information into the Insightly
# contact manager and tasks system. Some other hidden pages also demo how to read
# information out of Insightly, for example to display a list of tasks that are coming due. 
# 

import os
import string
import webapp2
import wsgiref.handlers

# import the required App Engine libraries, if you are hosting in a non-appengine environment
# you'll need to replace the Django templating engine
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

# import the Insightly SDK
from insightly import Insightly

# your Insightly API key goes here
apikey = 'your API key'

def load_page(page, data = None):
    """
    This helper function loads a Django template and merges data into it. The main.html file
    serves as a master template that child documents are merged into. 
    """
    if len(page) < 1: page = 'home'
    path = os.path.join(os.path.dirname(__file__), "main.html")
    if data is not None:
        if type(data) is dict:
            return template.render(path, data)
    data = dict(
        page = page + '.html',
    )
    return template.render(path, data)
        
class RequestInformationHandler(webapp2.RequestHandler):
    """
    This request handler implements the request information form, and handles the POST submission
    when the form is submitted.
    
    It adds the user to Insightly contacts, and also creates a task to follow up with the user. 
    """
    def get(self):
        self.response.out.write(load_page('request_information'))
    def post(self):
        i = Insightly(apikey = apikey)
        contactinfos = list()
        if len(self.request.get('EMAIL')) > 0:
            contactinfo = dict(
                TYPE = 'EMAIL',
                DETAIL = self.request.get('EMAIL'),
            )
            contactinfos.append(contactinfo)
        if len(self.request.get('PHONE')) > 0:
            contactinfo = dict(
                TYPE = 'PHONE',
                DETAIL = self.request.get('PHONE'),
            )
            contactinfos.append(contactinfo)
        contact = dict(
            SALUTATION = self.request.get('SALUTATION'),
            FIRST_NAME = self.request.get('FIRST_NAME'),
            LAST_NAME = self.request.get('LAST_NAME'),
            CONTACTINFOS = contactinfos,
        )
        contact = i.addContact(contact)
        
        if self.request.get('addtask') == 'y':
            task = dict(
                Title = 'Follow up with ' + self.request.get('FIRST_NAME') + ' ' + self.request.get('LAST_NAME'),
                PRIORITY = 2,
                STATUS = 'NOT STARTED',
                COMPLETED = False,
                OWNER_USER_ID = i.owner_id,
                VISIBLE_TO = 'EVERYONE',
                PUBLICLY_VISIBLE = True,
                RESPONSIBLE_USER_ID = i.owner_id,
            )
            task = i.addTask(task)
        self.redirect('/thankyou')
            
class ProjectsHandler(webapp2.RequestHandler):
    """
    This hidden request handler displays up to 50 projects in an unordered list. 
    """
    def get(self):
        i = Insightly(apikey = apikey)
        projects = i.getProjects(top=50)
        if len(projects) > 0:
            self.response.out.write('<ul>')
            for p in projects:
                self.response.out.write('<li>' + str(p.get('PROJECT_NAME','')))
            self.response.out.write('</ul>')
        
class TasksHandler(webapp2.RequestHandler):
    """
    This is a simple request handler that displays a list of upcoming tasks. 
    """
    def get(self):
        i = Insightly(apikey = apikey)
        tasks = i.getTasks(top=25, orderby='DUE_DATE desc')
        if len(tasks) > 0:
            self.response.out.write('<ul>')
            for t in tasks:
                self.response.out.write('<li>' + t.get('Title','No title') + ' Due: ' + t.get('DUE_DATE','') + '</li>')
            self.response.out.write('</ul>')
            
class PageHandler(webapp2.RequestHandler):
    """
    This is a generic request handler that serves pages to the path /nnnn, where the file merged into the master template
    is nnnn.html (see requestinformation.html for an example)
    """
    def get(self, page=''):
        self.response.out.write(load_page(page))

app = webapp2.WSGIApplication([
    ('/', RequestInformationHandler),
    ('/projects', ProjectsHandler),
    ('/requestinformation', RequestInformationHandler),
    ('/tasks', TasksHandler),
    (r'/(.*)', PageHandler)
], debug=True)

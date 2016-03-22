#
# Insightly - Python Sample Code
# Brian McConnell <brian@insight.ly>
#
# This sample code for shows how to build webapp2 compatible apps that integrate with Insightly.
# This will run as-is on Google App Engine for Python, and should also run on any webapp2
# runtime environment, although you will need to replace the App Engine django templating tools
# with the Django installation. In most cases this will easily run within the free quotas for
# App Engine, so you should be able to quickly modify this code and run it there.
#
# With the Python SDK you can access all of the major object types in Insightly, including:
#
# * Contacts
# * Emails
# * Events
# * LEads
# * Opportunities
# * Organizations
# * Projects
# * Tasks
#
# The sample app displays a simple form that prompts the user for contact information
# and then saves the information to Insightly as a contact or lead, and then creates a
# task to remind the assigned user to follow up with the newly created contact. 
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

# your Insightly API key goes here (don't share this publicly)
apikey = ''

def load_page(page, data = None):
    """
    This helper function loads a Django template and merges data into it. The main.html file
    serves as a master template that child documents are merged into. 
    """
    if len(page) < 1: page = 'home'
    path = os.path.join(os.path.dirname(__file__), "main.html")
    if data is not None:
        if type(data) is dict:
            if string.count(page, '.htm') > 0 :
                data['page'] = page
            else:
                data['page'] = page + '.html'
            return template.render(path, data)
    else:
        data = dict()
        if string.count(page, '.htm') > 0 :
            data['page'] = page
        else:
            data['page'] = page + '.html'
    return template.render(path, data)

def send_email(email):
    """
    This is a dummy function to send a thank you email to the user, add hooks to an email delivery
    service here (we recommend Mailgun)
    """
    return True

def spam_test(ip_address, text):
    """
    This is a dummy function to test if the form was submitted by a spambot. The Akismet service is
    a good way to do this. So insert a hook to your favorite spam/bot detection service here. Return
    True if the submission is flagged as spam.
    """
    return False

class ServePage(webapp2.RequestHandler):
    def get(self):
        """
        Serve the page with the data entry form to the user.
        """
        #
        # load a list of Insightly users, this is used to populate the assign to droplist,
        # to show an example of how to assign tasks to specific users.
        #
        i = Insightly(apikey = apikey)
        users = i.read('users')
        #
        # populate the dictionary passed into the Django template
        #
        data = dict(
            page = 'request_information.html',
            users = users,
        )
        #
        # render and serve the page, using Django templating
        #
        self.response.out.write(load_page('request_information.html', data=data))
    def post(self):
        """
        Process submitted form, create contact/lead and reminder task, serve response
        """
        #
        # get form fields
        #
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        organisation = self.request.get('organisation')
        phone = self.request.get('phone')
        email = self.request.get('email')
        website = self.request.get('website')
        comment = self.request.get('comment')
        addtask = self.request.get('addtask')
        saveas = self.request.get('saveas')
        responsible_user_id = self.request.get('responsible_user_id')
        
        #
        # This is a good place to check for spam/bot submissions using Akismet
        # or a captcha test like ReCaptcha. If the lead or contact is flagged as
        # spam, add a tag "spam". This way the user can decide keep or discard
        # these entries at their discretion, while easily flagged suspect entries
        # for review.
        #
        ip_address = self.request.remote_addr
        
        this_is_spam = spam_test(ip_address, comment)
        tags = list()
        if this is spam:
            tags.append({'TAG_NAME':'spam'})
    
        #
        # get the hidden field saveas, which can be contact or lead,
        # if omitted, saveas=lead
        #
        if saveas != 'contact' and saveas != 'lead':
            saveas = 'lead'
            
        if addtask == 'y' or addtask == 'Y':
            addtask = True
        else:
            addtask = False
            
        i = Insightly(apikey = apikey)
        
        if saveas == 'lead':
            lead = dict(
                FIRST_NAME = first_name,
                LAST_NAME = last_name,
                ORGANIZATION_NAME = organisation,
                PHONE_NUMBER = phone,
                EMAIL_ADDRESS = email,
                TAGS = tags,
            )
            i.create('leads', lead)
        else:
            contactinfos = list()
            if len(phone) > 0:
                contactinfo = dict(
                    TYPE = 'PHONE',
                    LABEL = 'Work',
                    DETAIL = phone,
                )
                contactinfos.append(contactinfo)
            if len(email) > 0:
                contactinfo = dict(
                    TYPE = 'EMAIL',
                    LABEL = 'Work',
                    DETAIL = email,
                )
                contactinfos.append(contactinfo)
            if len(website) > 0:
                contactinfo = dict(
                    TYPE = 'WEBSITE',
                    LABEL = 'Work',
                    DETAIL = website,
                )
                contactinfos.append(contactinfo)
            contact = dict(
                FIRST_NAME = first_name,
                LAST_NAME = last_name,
                CONTACTINFOS = contactinfos,
                BACKGROUND = comment,
                TAGS = tags,
            )
            i.create('contacts', contact)
        
        if addtask:
            task = dict(
                TITLE = 'Follow up with ' + first_name + ' ' + last_name,
                STATUS = 'Not Started',
                COMPLETED = False,
                PUBLICLY_VISIBLE = True,
                DETAILS = comment,
            )
            if len(responsible_user_id) > 0:
                task['RESPONSIBLE_USER_ID'] = int(responsible_user_id)
            i.create('tasks', task)
        
        data = dict(
            first_name = first_name,
            last_name = last_name,
            organisation = organisation,
            phone = phone,
            email = email,
            website = website,
        )
        
        #
        # render and serve the response page
        #
        
        self.response.out.write(load_page('thank_you.html', data = data))
        
        #
        # create and send an email to the user
        #
        
        if len(email) > 0 and string.count(email, '@') > 0:
            send_email(email)
        

app = webapp2.WSGIApplication([
    ('/', ServePage)], debug=True)

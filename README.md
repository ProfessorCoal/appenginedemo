appenginedemo
=============

Sample Insightly + Google App Engine Integration

This sample application implements a smart lead capture form which you can add to your website.

The application does the following:

* Displays a form the user fills in with their name, email, etc
* When the form is submitted, creates either a lead or contact using the data submitted
* Optionally creates a task, to remind a user to follow up with the prospect
* Displays a thank you message upon successful form submission
* Also includes hooks to dummy functions to send a thank you email and to do spam filtering

While this is a fairly simple demo program it will get you started and is easy to modify and
extend as needed. The program will run "out of the box" on Google App Engine, Google's popular
and easy to use cloud computing platform, and unless you expect a really high volume of submissions
should easily run within Google's free quota for the service.

Getting Started
===============

* Create a new App Engine project and local working directory for your project
* Copy the files into the directory
* Open main.py, and insert your API key in the variable api_key
* Open app.yaml and change the application name (in the first line in the config file) to your project name or ID
* Deploy the code to App Engine, and open the url https://your_app_name_or_id.appspot.com

That's all there is to it. If you have any questions, submit a support ticket at https://support.insight.ly
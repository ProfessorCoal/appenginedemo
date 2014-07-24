appenginedemo
=============

Sample Insightly + Google App Engine Integration

This sample app demonstrates how to integrate Insightly into Google App Engine projects. App Engine is an easy to use, yet highly scalable PaaS (platform as a service) environment. Unlike conventional colocation and virtual server environments (like AWS), App Engine virtually eliminates system administration and capacity planning for your projects.

You simply upload your Python code and a few configuration files, and App Engine provisions the resources needed to meet end user demand, and scales in real-time to match capacity with demand. 

The sample add implements a simple Twitter Bootstrap website with some sample content and a form to request more information. When you submit ther request for information form, it adds the person to your Insightly Contacts, and also creates a task to follow up with the user. Also included are some hidden pages that display upcoming tasks, recent projects, and so on. 

Getting Started
===============

* Create an application slot on App Engine for this project
* Download the project and unpack it into a local directory
* In the App Engine launcher app, select Add Existing Application
* Select the directory you extracted the project to
* Edit app.yaml to reference your apps slot name
* Click on Deploy
* Go to yourapp.appspot.com

You should see the home page and request information form.

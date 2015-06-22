#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import jinja2

import webapp2
import cgi
from google.appengine.ext import ndb


template_dir = os.path.join(os.path.dirname ('stage4-html'), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape= True)

class Greeting(ndb.Model):
    author = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

#Not sure but this may be another way to write above code to add to db.
#author = ndb.StringProperty()
#email = ndb.StringProperty()
#content = ndb.StringProperty()
#date = ndb.DateTimeProperty(auto_now_add=True)

#create objects to store to datastore. Need to "put" to save to db
#greet1 = Greeting(author = 'Steve', email='steveneels70@yahoo.com', content = 'DOM Structure')
#greet2 = Greeting(author = 'Steve', email='steveneels@att.net', content = 'Validation')

#greet1.put()
#greet2.put()

#allows computer time to save to database. Here waits for .1 sec.
#import time
#time.sleep(.1)

    

class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))


class MainPage(Handler):
    def write_form(self, error="",topic=""):
        self.response.out.write(form% {"error": error})
    
    def get(self):
        self.write_form()

    def post(self):
        items = self.request.get_all("topic")
        self.render("favorite_topic.html", items = items)
        topic=""
        if not topic:
            self.write_form("No topic was entered. Please try again!")
        else:
            self.response.out.write("Thank you for sharing!")
        
        

guestbook_key = ndb.Key('Guestbook', 'index4-html') #Do I still need this?

#To extract data from database. Uses router to tell users to go to mainpage and query to pull information.
class Guestbook(webapp2.RequestHandler):
    def get(self):

        #Check for error message
        error=self.request.get('error','')

        print '####'
        print error
        print '####'

        #Query the Datastore and order earliest date first
        query=Greeting.query().order(Greeting.date)
        
        #Test to print out all the greeting objects. .comment will print comments only
        print '####'
        for greeting in query:
            print greeting.comment
        print '####'

        greeting_list = query.fetch(5) # says fetch up to 5 greetings.Will see printed in the logs

    print '####'
    print len(greeting_list)
    print greeting_list(0).comment #comment will list comments only. without will list all attributes of object
    print greeting_list(1).comment
    print '####'
        
    def post(self):
        email=self.request.get('email')
        comment=self.request.get('comment')

        if email and comment:
            greeting=Greeting(email=email, comment=comment)
            greeting.put()

            import time
            time.sleep(.1)
            self.redirect('/')

        else:
            self.redirect(/?error=Please fill out the comment section!)
            
        greeting = Greeting()
        greeting.content = self.request.get("content")
        greeting.put()

        self.redirect('/', MainPage)


router = [('/',MainPage)]

    

app = webapp2.WSGIApplication ([('/', MainPage), (/'sign', Guestbook)],debug=True)

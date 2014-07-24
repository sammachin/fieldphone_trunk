import cherrypy
import os
from cherrypy.process import servers
from twilio import twiml
import urllib



def fake_wait_for_occupied_port(host, port): 
	return

servers.wait_for_occupied_port = fake_wait_for_occupied_port

class Start(object):
	def call(self, var=None, **params):
		r = twiml.Response()
		r.say("Welcome to field phone, please enter the number you wish to dial")
		r.gather(numDigits=5, action="/route", method="POST")
		return str(r)
	def route(self, var=None, **params):
		number = urllib.unquote(cherrypy.request.params['Digits'])
		r = twiml.Response()
		d = twiml.Dial()
		d.sip("sip:%s@phone.emf.camp:9252" % number)
		r.append(d)
		return str(r)
	call.exposed = True
	route.exposed = True

cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.quickstart(Start())



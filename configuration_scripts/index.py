#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
from yattag import Doc
from yattag import indent
import requests
cgitb.enable()
print "Content-Type: text/html;charset=utf-8"
print
print "<!DOCTYPE html>"

url ='http://IP:5984/accounts/_design/top_balance/_view/top_balance'
response =requests.get(url, auth=(***REMOVED***,***REMOVED***))
data = response.json()
balancedict={}
for key,value in data.iteritems() : 
	if isinstance(value, list) : 
		for element in value : 
			balancedict.update({element['key']: element['value']})


sortedlist= sorted(balancedict.items(), key=lambda x:x[1], reverse=True)
resultdict={}

doc,tag, text=Doc().tagtext()
with tag('html'):
	with tag('head') : 
		#with tag('link',('rel','stylesheet'),('type','text/css'),('href','mystyle.css')) :
		print '<link rel="stylesheet" type="text/css" href="mystyle.css">'
	with tag('body'):
		with tag('h1'):
			text('Uptime Challenge Top User Balance')
		with tag('table',('border', '1'),('style','width:50%')):
			with tag('tr') :
				with tag('td', ('style', 'font-weight:bold')) :
					text('Group')
				with tag('td',('style','font-weight:bold')) :
					text('Balance')
			for i,(a,b) in enumerate(sortedlist) :
				with tag('tr')	:
					with tag('td'):
						text(str(a))
					with tag('td'):
						text(str(b))
print indent(doc.getvalue())

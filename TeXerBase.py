#!/usr/bin/python3
#coding: utf-8
'''
Base file of TeXerBase - a Database Server for Exercises
'''

import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart   
from urllib.parse import parse_qs
import json
from jinja2 import Template
from multiprocessing import Process

from modules import dbio, mdTeX2html, getHtml

# global settings:

dbfile = "database.db"
webServerPort = 8081

# WebServer stuff:

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    ''' HTTPRequestHandler class '''
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_HEAD(s):
        self._set_headers;
    
    def do_GET(self):
        ''' The GET-Handler returns a certain exercice '''
        if self.path.startswith('/img/'):
            self.sendStatic()
            return
        self._set_headers()
        with open('template/base.tpl') as f:
            basetemplate = Template(f.read())
        
        # switch for the path:
        if self.path == '/':
            content = getHtml.getStart(db.getSubjects())
        elif self.path == '/test':
            content = '<p>Dein Pfad: %s</p><br />\n' % self.path
            content += getHtml.getTest()
        elif self.path == '/cheatsheetSvg':
            with open('template/cheatsheetSvg.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render()
        elif self.path == '/cheatsheetMdTeX':
            with open('template/cheatsheetMdTeX.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render()
        elif self.path.startswith('/newExercise/'):
            topics = db.getTopics(self.path.strip('/newExercise/'))
            with open('template/newExercise.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(topics=topics, licenses=db.getLicenses())
        elif self.path == '/saveNewExercise':
            content = 'ERROR: expected POST, not GET on this path!'
        elif self.path.startswith('/viewExerciseList/'):
            sid = self.path.strip('/viewExerciseList/')
            exerlist = db.getExerciseList(sid)
            topics = db.getTopics(sid)
            content = getHtml.viewExerciseList(exerlist=exerlist, topics=topics)
        elif (self.path.startswith('/viewExercise/') 
                and self.path.strip('/viewExercise/').isnumeric()):
            eid = self.path.strip('/viewExercise/')
            exercise = db.getExercise(eid)
            content = getHtml.viewExercise(exercise)
        elif (self.path.startswith('/editExercise/') 
                and self.path.strip('/editExercise/').isnumeric()):
            eid = self.path.strip('/editExercise/')
            exercise = db.getExercise(eid)
            topics = db.getTopics()
            licenses = db.getLicenses()
            with open('template/editExercise.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(exercise=exercise, topics=topics, licenses=licenses)
        elif self.path.startswith('/sheet/'):
            # Example: /sheet/Title;1,2,3;solutions
            # options: '', 'solutions' and 'source'
            # TODO: create a sepatate def for this, returning a "url-Builder"-page by default or if illeral url
            title = self.path.strip('/sheet/').split(';')[0]
            exes = self.path.strip('/sheet/').split(';')[1].split(',')
            exes = list(map(int, exes))
            exercises = db.getExercises(exes)
            option = self.path.strip('/sheet/').split(';')[2]
            content = getHtml.getSheet(title, exercises, option)
        else:
            content = 'ERROR 404: The path was not found by TeXerBase'
            content += '<p>Your path: %s</p><br />\n' % self.path
        
        # Write content as utf-8 data
        out = basetemplate.render(content=content)
        self.wfile.write(bytes(out, "utf8"))
        return
    
    def sendStatic(self):
        '''send a static file from img or static-folder'''
        try:
            #Check the file extension required and
            #set the right mime type
            sendReply = False
            # Images:
            if self.path.startswith('/img/'):
                if self.path.endswith(".jpg"):
                    mimetype='image/jpg'
                    sendReply = True
                if self.path.endswith(".png"):
                    mimetype='image/png'
                    sendReply = True
                if self.path.endswith(".svg"):
                    mimetype='image/svg+xml'
                    sendReply = True
            # static files:
            elif self.path.startswith('/static/'):
                if self.path.endswith(".js"):
                    mimetype='application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype='text/css'
                    sendReply = True
                f = open(self.path) 
            if sendReply == True:
                #Open the static file requested and send it
                fipath = (str(os.getcwd())+self.path)
                f = open(fipath, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length).decode('utf-8'), 
                    keep_blank_values=1)
        elif ctype == 'application/mdtex':
            length = int(self.headers['content-length'])
            postvars = self.rfile.read(length).decode('utf-8')
        else:
            postvars = {}
        return postvars
    
    def do_POST(self):
        ''' all operations on an exercise like editing is done via POST-Requests '''
        self._set_headers()
        postvars = self.parse_POST()
        # path-switch, quick answer if just mdtex2html
        if self.path == '/mdtex2html':
            try:
                result = mdTeX2html.convert(postvars)
            except Exception as e:
                result = 'ERROR: Could not convert the mdTeX to HTML:' + str(e)
            self.wfile.write(bytes(result, "utf8"))
            return
        elif self.path == '/saveNewExercise':
            result = db.insertExercise(postvars)
        #else:
        elif self.path == '/saveExercise':
            result = db.editExercise(postvars)
        
        with open('template/base.tpl') as f:
            basetemplate = Template(f.read())
        # Build the answer content:
        if result == 'exists':
            content = '<h1 style="color:red;">Fehler!</h1>\n'
            content += '<p>Der Titel der Aufgabe existiert schon.</p>\n'
            content += '<p><a href="javascript:history.back()">Gehe zurück</a> oder bearbeite die existierende Aufgabe.</p>\n'
        elif str(result).isdigit():
            content = '<h1 style="color:green;">Erfolg!</h1>\n'
            content += '<p>Die folgende Aufgabe wurde erfolgreich in die TeXerBase-Datenbank eingetragen:</p>\n'
            content += '<h1>%s</h1>\n'%postvars['title'][0]
            content += '<p>Aufgabe <a href="editExercise/%s">bearbeiten</a> oder <a href="viewExercise/%s">Anzeigen</a></p>' % (result, result)
        else:
            content = '<h1 style="color:red;">500: Server-error in POST-path!</h1>\n' + result
        
        # Write content as utf-8 data
        out = basetemplate.render(content=content)
        self.wfile.write(bytes(out, "utf8"))
        return

def runWebServer():
    ''' start the webserver '''
    print('starting server')
    server_address = ('127.0.0.1', webServerPort)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('server is running')
    httpd.serve_forever()

# get it started:

db = dbio.ExerDb(dbfile)

webServer = Process(target=runWebServer, args=())
webServer.start()

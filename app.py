#!/usr/bin/python3
#coding: utf-8
'''
Base file of TeXerBase - a Database Server for Exercises
'''

import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart   
from urllib import parse
import json
from jinja2 import Template
from multiprocessing import Process

import mdtex2mathml as mdTeX2html
from modules import dbio, getHtml

# global settings:

dbfile = "texerbase.sqlite3"
webServerPort = 4203

# WebServer stuff:

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    ''' HTTPRequestHandler class '''
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
    def do_HEAD(s):
        self._set_headers;
    
    def do_GET(self):
        ''' The GET-Handler returns a certain exercise '''
        if self.path.startswith('/img/') or self.path.startswith('/static/'):
            self.sendStatic()
            return
        self._set_headers()
        with open('template/base.tpl') as f:
            basetemplate = Template(f.read())
        with open('template/nav.tpl') as f:
            nav = Template(f.read())
        relroot = './'
        
        # switch for the path:
        if self.path == '/':
            content = getHtml.getStart(db.getSubjects(), db.getTopics(), db.getExerciseList())
        elif self.path == '/reloadDb':
            db.reloadDb(dbfile)
            content = '<p>Datenbank erfolgreich neu geladen!</p><br />\n'
        elif self.path == '/test':
            content = '<p>Dein Pfad: %s</p><br />\n' % self.path
            content += getHtml.getTest()
        elif self.path == '/svgCheatsheet':
            with open('template/svgCheatsheet.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render()
        elif self.path == '/mdTeXCheatsheet':
            with open('template/mdTeXCheatsheet.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render()
        elif self.path.startswith('/exercise/'):
            relroot = '../'
            if self.path.strip('/exercise/').isnumeric():
                eid = self.path.strip('/exercise/')
                e = db.getExercise(eid)
            else:
                e = {'id': '', 'title': '', 'topicId': '', 'difficulty': 0, 'exercise': '', 'solution': '', 'origin': '', 'author': '', 'year': '', 'licenseId': 0, 'comment': '', 'zOrder': 0}
            eJson = json.dumps(e)
            #content = getHtml.getExercise(e)
            with open('template/exercise.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(e=e, eJson = eJson, relroot=relroot)
        elif self.path.startswith('/sheetNew/'):
            relroot = '../'
            sid = self.path.strip('/sheetNew/')
            exerlist = db.getExerciseList(sid)
            topics = db.getTopics(sid)
            with open('template/sheetNew.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(exerlist=exerlist, topics=topics)
        elif self.path.startswith('/sheet/'):
            relroot = '../'
            title = parse.unquote(self.path.strip('/sheet/').split(';')[0])
            exeStrings = self.path.strip('/sheet/').split(';')[1].split(',')
            exeInts = []
            for item in exeStrings:
                try:
                    i = int(item)
                    exeInts.append(i)
                except:
                    pass
            exercises = db.getExercises(exeInts)
            option = self.path.strip('/sheet/').split(';')[2]
            content = getHtml.getSheet(title, exercises, option)
            #nav = ''
        # TODO: einen /public-Teil, in den Sheets geeignet bereitgestellt werden können.
        # TODO dazu: Speichermöglichkeit für sheets in der DB!
        else:
            content = 'ERROR 404: The path was not found by TeXerBase'
            content += '<p>Your path: %s</p><br />\n' % self.path
        
        # Write content as utf-8 data
        out = basetemplate.render(relroot=relroot, nav=nav.render(relroot=relroot), content=content)
        self.wfile.write(bytes(out, 'utf8'))
        return
    
    def sendStatic(self):
        '''send a static file from img or static-folder'''
        try:
            #Check the file extension required and set the right mime type
            sendReply = False
            # Images:
            if self.path.startswith('/img/'):
                if self.path.endswith(".jpg"):
                    mimetype='image/jpg'
                    sendReply = True
                elif self.path.endswith(".png"):
                    mimetype='image/png'
                    sendReply = True
                elif self.path.endswith(".svg"):
                    mimetype='image/svg+xml'
                    sendReply = True
            # static files:
            elif self.path.startswith('/static/'):
                if self.path.endswith(".js"):
                    mimetype='application/javascript'
                    sendReply = True
                elif self.path.endswith(".css"):
                    mimetype='text/css'
                    sendReply = True
                elif self.path.endswith('.woff2'):
                    mimetype = 'application/font-woff2'
                    sendReply = True
            if sendReply == True:
                #Open the static file requested and send it
                fipath = (str(os.getcwd())+self.path)
                f = open(fipath, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                self.send_error(501,'unsupported file type on path %s' % self.path)
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            postvars = json.loads(self.rfile.read(length).decode('utf-8'))
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
        
        # path-switch
        if self.path == '/mdtex2html':
            try:
                result = mdTeX2html.convert(postvars)
            except Exception as e:
                result = 'ERROR: Could not convert the mdTeX to HTML:' + str(e)
        elif self.path == '/getExerciseJson':
            e = db.getExercise(postvars)
            result = json.dumps(e)
        elif self.path == '/getTopicsJson':
            t = db.getTopics()
            result = json.dumps(t)
        elif self.path == '/getLicensesJson':
            l = db.getLicenses()
            result = json.dumps(l)
        elif self.path == '/saveExercise':
            print(postvars)
            if postvars['id'] == '':
                result = str(db.insertExercise(postvars))
            elif postvars['id'].isnumeric():
                result = db.editExercise(postvars)
        self.wfile.write(bytes(result, "utf8"))
        return

def runWebServer():
    ''' start the webserver '''
    print('starting server')
    server_address = ('127.0.0.1', webServerPort)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('server is running on port ' + str(webServerPort))
    httpd.serve_forever()

# get it started:

db = dbio.ExerDb(dbfile)

webServer = Process(target=runWebServer, args=())
webServer.start()

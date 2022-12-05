#!/usr/bin/python3
#coding: utf-8
'''
Base file of TeXerBase - a Database Server for Exercises
'''

import os
import sqlite3
from flask import Flask, render_template, request, send_from_directory, make_response, jsonify
import json, string
from jinja2 import Template
from multiprocessing import Process
import mdtex2html
from datetime import date

from modules import dbio, getHtml

# global settings:

dbfile = "texerbase.sqlite3"
host = '0.0.0.0'
debug = 'true'
extensions = ['def_list', 'fenced_code', 'md_in_html', 'tables', 'admonition', 'nl2br', 'sane_lists', 'toc'] #TODO: insert list of allowed extensions
imgFolder = 'images'

# WebServer stuff:

app = Flask(__name__)

@app.route('/static/<path:path>', methods=['GET'])
def sendStatic(path):
    return send_from_directory('', path)

@app.route('/img/<path:path>', methods=['GET'])
def sendImg(path):
    return send_from_directory('images/', path)
    
@app.route('/', methods=['GET'])
def index():
    '''show index-page'''
    # TODO: return settings if first run (no database)
    relroot = './'
    db = dbio.ExerDb(dbfile)
    subjects = db.getSubjects()
    topics = db.getTopics()
    exes = db.getExerciseList()
    #content = getHtml.getStart(db.getSubjects(), db.getTopics(), db.getExerciseList())#deprecated, rendering in frontend now
    return render_template('index.html', relroot=relroot, subjects=subjects, topics=topics, exes=exes)

@app.route('/changeZ', methods=['PATCH'])
def patch_changeZ():
    '''change zOrder of an exercise'''
    pv = request.json
    #print(pv)
    db = dbio.ExerDb(dbfile)
    db.exerZMove(pv['tid'], pv['eid'], pv['direction'])
    topic = db.getTopic(pv['tid'])
    exerciseList = db.getExerciseList('', topic['id'])
    result = getHtml.getExerciseTable(exerciseList, topic)#TODO: send data as json
    #content = getHtml.getStart(db.getSubjects(), db.getTopics(), db.getExerciseList())
    return result

@app.route('/reloadDb', methods=['GET'])
def reloadDb():
    '''reload database'''
    relroot = './'
    db = dbio.ExerDb(dbfile)
    db.reloadDb(dbfile)
    db.topicZIndexNormalize(1)
    content = '<p>Datenbank erfolgreich neu geladen!</p><br />\n'
    return render_template('index.html', relroot=relroot, content=content)

@app.route('/test', methods=['GET'])
def sendTest():
    '''show test-page'''
    relroot = './'
    db = dbio.ExerDb(dbfile)
    content = '<p>Dein Pfad: %s</p><br />\n' % self.path
    content += getHtml.getTest()
    return render_template('index.html', relroot=relroot, content=content)

@app.route('/mdTeXCheatsheet/', methods=['GET'])
def SendMdTeXCheatsheet():
    '''show mdTeXCheatsheet-page'''
    relroot = '../'
    db = dbio.ExerDb(dbfile)
    return render_template('mdTeXCheatsheet.html', relroot=relroot)

@app.route('/exercise/', methods=['GET'])
def sendNewExercise():
    '''show exercise'''
    relroot = '../'
    db = dbio.ExerDb(dbfile)
    e = {'id': '', 'title': '', 'topicId': '', 'difficulty': 0, 'exercise': '', 'solution': '', 'origin': 'self', 'author': '', 'year': str(date.today().year), 'licenseId': 2, 'comment': '', 'zOrder': 0}
    eJson = json.dumps(e)
    return render_template('exercise.html', relroot=relroot, e=e, eJson = eJson)

@app.route('/exercise/<string:eid>', methods=['GET'])
def sendExercise(eid):
    '''show exercise'''
    relroot = '../'
    db = dbio.ExerDb(dbfile)
    if eid.isnumeric():
        e = db.getExercise(eid)
    else:
        return 'ERROR 404: Exercise not found!'
    eJson = json.dumps(e)
    return render_template('exercise.html', relroot=relroot, e=e, eJson = eJson)

@app.route('/exercise/<string:eid>', methods=['DELETE'])
def deleteExercise(eid):
    '''delete exercise'''
    relroot = '../'
    db = dbio.ExerDb(dbfile)
    if eid.isnumeric():
        result = db.deleteExercise(eid)
    else:
        return 'ERROR: no valid exercise id!'
    return result

@app.route('/sheetNew/<string:sid>', methods=['GET'])
def sendSheetNew(sid):
    '''show sheetNew-page'''
    relroot = '../'
    db = dbio.ExerDb(dbfile)
    exerlist = db.getExerciseList(sid)
    topics = db.getTopics(sid)
    return render_template('sheetNew.html', relroot=relroot, exerlist=exerlist, topics=topics)

@app.route('/images/', methods=['GET'])
def imgages():
    files = os.listdir(imgFolder)
    #print(json.dumps(files, indent=4, sort_keys=True)) # show files-dict for debugging and reference
    images = json.dumps(files)
    return render_template('images.html', relroot='../', images=images)

@app.route('/imgUpload/', methods=['GET'])
def imgUpload():
    return render_template('imgUpload.html', relroot='../')
@app.route('/imgUpload/<path:fname>', methods=['POST'])
def imgUploadPost(fname):
    safechars = string.ascii_lowercase + string.ascii_uppercase + string.digits + '.-_'
    fname = ''.join([c for c in fname if c in safechars])
    meta = False
    filepath = os.path.join(imgFolder, fname)
    if os.path.isfile(filepath):
        return 'ERROR 409: file exists!'
    else:
        uploadFile = request.files['file']
        uploadFile.filename == fname
        uploadFile.save(filepath)
        return filepath

@app.route('/sheet/<string:sheet>', methods=['GET'])
def sendSheet(sheet):
    '''show sheet-page'''
    relroot = '../'
    db = dbio.ExerDb(dbfile)
    title = sheet.split(';')[0]
    exeStrings = sheet.split(';')[1].split(',')
    exeInts = []
    for item in exeStrings:
        try:
            i = int(item)
            exeInts.append(i)
        except:
            pass
    exercises = db.getExercises(exeInts)
    option = sheet.split(';')[2]
    #nav = ''
    content = getHtml.getSheet(title, exercises, option)
    return render_template('index.html', relroot=relroot, content=content)

@app.route('/mdtex2html', methods=['POST'])
def post_mdtex2html():
    postvars = request.data
    try:
        return mdtex2html.convert(postvars.decode("utf-8"), extensions)
    except Exception as e:
        return 'ERROR: Could not convert the mdTeX to HTML:' + str(e)

@app.route('/getExerciseHtml', methods=['POST'])
def post_getExerciseHtml():
    db = dbio.ExerDb(dbfile)
    postvars = request.data
    e = db.getExercise(postvars.decode("utf-8"))
    exer = mdtex2html.convert(e['exercise'], extensions)
    return exer

@app.route('/getExerciseJson', methods=['POST'])
def post_getExerciseJson():
    db = dbio.ExerDb(dbfile)
    postvars = request.data
    e = db.getExercise(postvars)
    return json.dumps(e)

@app.route('/getTopicsJson', methods=['POST'])
def post_getTopicsJson():
    db = dbio.ExerDb(dbfile)
    postvars = request.data
    t = db.getTopics()
    return json.dumps(t)

@app.route('/getLicensesJson', methods=['POST'])
def post_getLicensesJson():
    db = dbio.ExerDb(dbfile)
    postvars = request.data
    l = db.getLicenses()
    return json.dumps(l)

@app.route('/saveExercise', methods=['POST'])
def post_saveExercise():
    db = dbio.ExerDb(dbfile)
    postvars = json.loads(request.data)
    if postvars['id'] == '':
        return str(db.insertExercise(postvars))
    elif postvars['id'].isnumeric():
        return db.editExercise(postvars)

# init-stuff:

def initStuff():
    ''' make sure everything is set up and tidy '''
    if not os.path.exists(imgFolder):
        os.makedirs(imgFolder)
    db = dbio.ExerDb(dbfile)
    topics = db.getTopics()
    for t in topics:
        db.topicZIndexNormalize(t['id'])
initStuff()

# run it:

if __name__ == '__main__':
    app.run(host=host, debug=debug)

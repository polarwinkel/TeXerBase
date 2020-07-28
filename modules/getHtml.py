#!/usr/bin/python3
'''
This will build and return some html-code-snippets for TeXerBase.

Some pages are directly build with a jinja2-template, 
see those if you don't find it here.

The output language is german.
'''

from modules import mdTeX2html
from jinja2 import Template

def getStart(subjects, topics, exerciseList):
    '''returns the html for the startpage'''
    result = '<h1>TeXerBase Aufgabendatenbank</h1>\n'
    result = '<h2>Vorhandene Aufgaben:</h2>\n'
    for sub in subjects:
        #result += '<p><a href="viewExerciseList/%s">%s</a></p>\n' % (sub['id'], sub['subject'])
        result += '<details><summary style="font-size:1.4em; font-weight: bold;">%s</summary><ul>\n' % sub['subject']
        for topic in topics:
            if topic['subjectId'] == sub['id']:
                result += '<li><details><summary>%s</summary>\n' % topic['topic']
                result += getExerciseTable(exerciseList, topic)
                result += '</details>'
        result += '</details>'
    result += '<p><a href="./exercise/">Neue Aufgabe erstellen</a></p>'
    result += '<h2>Aufgabenblatt erstellen:</h2>\n'
    for sub in subjects:
        result += '<p><a href="sheetNew/%s">%s</a></p>\n' % (sub['id'], sub['subject'])
    return result

def getExerciseTable(exerciseList, topic):
    ''' returns an overview of exercises for a topic'''
    result = '<table><tr>\n'
    result += '<th style="width:80%">Titel</th>\n'
    result += '<th>Schwierigkeit</th>\n'
    result += '</tr>\n'
    for exe in exerciseList:
        if exe['topicId']==topic['id']:
            result += '<tr>\n'
            result += '<td><a href="./exercise/%s">' % exe['id'] + exe['title'] + '</a></td>\n'
            result += '<td>' + str(exe['difficulty']) + '</td>\n'
            result += '</tr>\n'
    result += '</table>\n'
    return result

def getExercise(exercise):
    '''returns an html-representation of an exercise'''
    result = '<h1>%s</h1>\n' % exercise['title']
    result += mdTeX2html.convert(exercise['exercise'])
    if exercise['solution'] != '':
        result += '<hr />\n'
        result += '<h1>Lösung</h1>\n'
        result += mdTeX2html.convert(exercise['solution'])
    if exercise['origin'] != '':
        result += '<p style="text-align:right;">Quelle: %s</p>\n' % exercise['origin']
    if exercise['comment'] != '':
        result += '<hr />\n'
        result += '<h2>Bemerkungen</h2>\n'
        result += mdTeX2html.convert(exercise['comment'])
    result += '<p style="text-align:right;" class="no-print"><a href="../exerciseEdit/%s">Aufgabe bearbeiten</a></p>\n' % exercise['id']
    return result

def getSheet(title, exercises, option):
    ''' returns a sheet with exercises/solutions/source according to options '''
    result = '<h1>%s</h1>' % title
    i = 1
    if option=='exercises' or option=='':
        for ex in exercises:
            result += '<h2>Aufgabe %s: %s</h2>' % (str(i), ex['title'])
            result += mdTeX2html.convert(ex['exercise'])
            i+=1
    elif option == 'solutions':
        for ex in exercises:
            result += '<h2>Aufgabe %s: %s</h2>' % (str(i), ex['title'])
            result += mdTeX2html.convert(ex[5])
            i+=1
    elif option == 'source':
        for ex in exercises:
            result += '<pre>'
            result += '# '+ex['title']+'<br />\n'
            result += ex['exercise']
            result += '</pre><br />\n'
    else:
        result = '<p style="color:red;">ERROR 404: Illegal URL, I didn\'t understand your option!</p>'
    return result

def getTest():
    '''returns a Testpage, rendered from the test.mdtex in test folder'''
    with open('test/test.mdtex', 'r') as f:
        mdtex = f.read()
    result = mdTeX2html.convert(mdtex)
    result += '<br>\n'
    result += 'Webrequest-Test:<br>\n'
    result += '<div id="requestbox">Ursprünglicher Requestbox-Testinhalt</div>\n'
    result += '<button onClick="request();">request-test</button>\n'
    return result

#!/usr/bin/python3
'''
This will build and return the html-code for TeXerBase.

Some pages are directly build with a jinja2-template, 
see those if you don't find it here.
'''

from modules import mdTeX2html
from jinja2 import Template

def getStart(subjects):
    '''returns the html for the startpage'''
    result = '<h1>TeXerBase Startseite</h1>\n'
    result += '<h2>Aufgaben anzeigen:</h2>\n'
    for sub in subjects:
        result += '<p><a href="viewExerciseList/%s">%s</a></p>\n' % (sub[0], sub[1])
    result += '<h2>Aufgaben hinzufügen:</h2>\n'
    for sub in subjects:
        result += '<p><a href="newExercise/%s">%s</a></p>\n' % (sub[0], sub[1])
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

def viewExerciseList(exerlist, topics):
    result = '<h1>Vorhandene Aufgaben</h1>\n'
    result += '<table>\n'
    result += '<tr>\n'
    result += '<th style="width:80%">Titel</th>\n'
    result += '<th>Schwierigkeit</th>\n'
    result += '</tr>\n'
    for topic in topics:
        result += '<tr><td><h3>%s</h3></td></tr><tr><td></td></tr>\n' % topic[2]
        for item in exerlist:
            if item[2]==topic[0]:
                result += '<tr>\n'
                result += '<td><a href="../viewExercise/%s">' % item[0] + item[1] + '</a></td>\n'
                result += '<td>' + str(item[3]) + '</td>\n'
                result += '</tr>\n'
    result += '</table>\n'
    return result

def viewExercise(exercise):
    '''returns an html-representation of an exercise'''
    result = '<h1>%s</h1>\n' % exercise[1]
    result += mdTeX2html.convert(exercise[4])
    if exercise[5] != '':
        result += '<hr />\n'
        result += '<h1>Lösung</h1>\n'
        result += mdTeX2html.convert(exercise[5])
    if exercise[6] != '':
        result += '<p style="text-align:right;">Quelle: %s</p>\n' % exercise[6]
    if exercise[10] != '':
        result += '<hr />\n'
        result += '<h2>Bemerkungen</h2>\n'
        result += mdTeX2html.convert(exercise[10])
    result += '<p style="text-align:right;" class="no-print"><a href="../editExercise/%s">Aufgabe bearbeiten</a></p>\n' % exercise[0]
    return result

def getSheet(title, exercises, option):
    '''
        returns a sheet with the exercises
        A given string 'solutions' or 'source' semicolon-separated at the end
        will return according pages.
    '''
    result = '<h1>%s</h1>' % title
    i = 1
    if option=='exercises' or option=='':
        for ex in exercises:
            result += '<h2>Aufgabe %s</h2>' % str(i)
            result += mdTeX2html.convert(ex[4])
            i+=1
    elif option == 'solutions':
        for ex in exercises:
            result += '<h2>Aufgabe %s</h2>' % str(i)
            result += mdTeX2html.convert(ex[5])
            i+=1
    elif option == 'source':
        result += '<code>'
        for ex in exercises:
            result += ex[4]
        result += '</code>'
    else:
        result = '<p style="color:red;">ERROR 404: Illegal URL.</p>'
    return result

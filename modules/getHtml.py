#!/usr/bin/python3
'''
This will build and return some html-code-snippets for TeXerBase.

Some pages are directly build with a jinja2-template, 
see those if you don't find it here.

The output language is german.
'''

import mdtex2html
from jinja2 import Template

def getStart(subjects, topics, exerciseList):#deprecated
    '''returns the html for the startpage'''
    result = '<h1>TeXerBase Exercise Database</h1>\n'
    result += '<h2>Exercises:</h2>\n'
    for sub in subjects:
        #result += '<p><a href="viewExerciseList/%s">%s</a></p>\n' % (sub['id'], sub['subject'])
        result += '<details><summary style="font-size:1.4em; font-weight: bold;">%s</summary><ul>\n' % sub['subject']
        for topic in topics:
            if topic['subjectId'] == sub['id']:
                result += '<li><details><summary>%s</summary>\n' % topic['topic']
                result += getExerciseTable(exerciseList, topic)
                result += '</details>'
        result += '</details>'
    result += '<p><a href="./exercise/">Create New Exercise</a></p>'
    result += '<h2>Create New Sheet:</h2>\n'
    for sub in subjects:
        result += '<p><a href="sheetNew/%s">%s</a></p>\n' % (sub['id'], sub['subject'])
    return result

def getExerciseTable(exerciseList, topic):# may become deprecated, still needed for changeZ
    ''' returns an overview of exercises for a topic'''
    result = '<table><tr>\n'
    result += '<th style="width:1em;"></th>'
    result += '<th style="width:2em;"></th>'
    result += '<th style="width:80%">Titel</th>\n'
    result += '<th>Schwierigkeit</th>\n'
    result += '</tr>\n'
    for exe in exerciseList:
        if exe['topicId']==topic['id']:
            result += '<tr id="etr'+str(exe['id'])+'">\n'
            result += '<td style="vertical-align: top;"><a onclick="loadExercise('+str(exe['id'])+')">+</a></td>\n'
            result += '<td><a onclick="move('+str(topic['id'])+', '+str(exe['id'])+', -1, this)">&uarr;</a>'
            result += '/<a onclick="move('+str(topic['id'])+', '+str(exe['id'])+', 1, this)">&darr;</a></td>\n'
            result += '<td><a href="./exercise/%s">' % exe['id'] + exe['title'] + '</a></td>\n'
            result += '<td>' + str(exe['difficulty']) + '</td>\n'
            result += '</tr>\n'
    result += '</table>\n'
    return result

def getSheet(title, exercises, option):
    ''' returns a sheet with exercises/solutions/source according to options '''
    result = '<h1>%s</h1>' % title
    i = 1
    if option=='exercises' or option=='':
        for ex in exercises:
            result += '<h2>Exercise %s: %s</h2>' % (str(i), ex['title'])
            result += mdtex2html.convert(ex['exercise'])
            i+=1
    elif option == 'solutions':
        for ex in exercises:
            result += '<h2>Exercise %s: %s</h2>' % (str(i), ex['title'])
            solution = mdtex2html.convert(ex['solution'])
            if solution == '':
                result += '[no solution given]'
            else:
                result += solution
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
    result = mdtex2html.convert(mdtex)
    result += '<br>\n'
    result += 'Webrequest-Test:<br>\n'
    result += '<div id="requestbox">Initial Requestbox-Testcontent</div>\n'
    result += '<button onClick="request();">request-test</button>\n'
    return result

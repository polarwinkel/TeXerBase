#!/usr/bin/python3
'''
Database-IO-file of TeXerBase - an Database Server for Exercises
'''

import sqlite3
import os
from modules import dbInit

class ExerDb:
    ''' Database-Connection to the TeXerBase-Database '''
    def __init__(self, dbfile):
        if not os.path.exists(dbfile):
            connection = sqlite3.connect(dbfile)
            cursor = connection.cursor()
            # activate support for foreign keys in SQLite:
            sql_command = 'PRAGMA foreign_keys = ON;'
            cursor.execute(sql_command)
            connection.commit()
            connection.close()
        self._connection = sqlite3.connect(dbfile) # _x = potected, __ would be private
        dbInit.checkTables(self)
        dbInit.checkSubjects(self)
        dbInit.checkLicenses(self)
    
    def reloadDb(self, dbfile):
        '''reloads the database file, i.e. after external changes/sync'''
        self._connection.commit() # not necessary, just to be sure
        self._connection.close()
        self._connection = sqlite3.connect(dbfile)
    
    def checkTitle(self, title):
        '''checks if a title is taken already for an exercise and returns the id or -1'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM exercises WHERE title=?'''
        cursor.execute(sqlTemplate, (title, ))
        exerId = cursor.fetchone()
        if exerId is None:
            return -1
        else:
            return exerId[0]
    
    def insertExercise(self, e):
        ''' inserts an exercise, received as dictionary, into the database,
                returns 'success', the existing title-id if title is taken or the SQL-Error '''
        # TODO: check integrity - here?
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM exercises WHERE title=?'''
        cursor.execute(sqlTemplate, (e['title'], ))
        if cursor.fetchone():
            return 'ERROR: Title exists already. Choose a different one!'
        sqlTemplate = '''INSERT INTO exercises 
                (title, topicId, difficulty, exercise, solution, origin, author, year, licenseId, comment, zOrder) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        valuelist = (e['title'],
                    e['topicId'],
                    e['difficulty'],
                    e['exercise'],
                    e['solution'],
                    e['origin'],
                    e['author'],
                    e['year'],
                    e['licenseId'],
                    e['comment'],
                    e['zOrder']
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        exerId = self.checkTitle(e['title'])
        self.topicZIndexNormalize(e['topicId'])
        if exerId >= 0:
            return exerId
        else:
            return 'ERROR 500: Unknown server error after entering into database'
    
    def editExercise(self, e):
        ''' edits an exercise, received as dictionary, into the database '''
        # TODO: check integrity - here?
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE exercises 
                SET title=?, topicId=?, difficulty=?, exercise=?, solution=?, origin=?, author=?, year=?, licenseId=?, comment=?, zOrder=?
                WHERE id=?;'''
        valuelist = (e['title'],
                    e['topicId'],
                    e['difficulty'],
                    e['exercise'],
                    e['solution'],
                    e['origin'],
                    e['author'],
                    e['year'],
                    e['licenseId'],
                    e['comment'],
                    e['zOrder'],
                    e['id']
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
            result = e['id']
        except sqlite3.OperationalError as err:
            args = list(err.args)
            result = 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return result
    
    def deleteExercise(self, eid):
        ''' delete an exercise '''
        cursor = self._connection.cursor()
        sqlTemplate = '''DELETE FROM exercises 
                WHERE id=?;'''
        try:
            cursor.execute(sqlTemplate, eid)
            result = 'ok'
        except sqlite3.OperationalError as err:
            args = list(err.args)
            result = 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return result
    
    def getExerciseList(self, sid='', tid='', searchword=''):
        '''returns a List of exercises (as dict) matching the filter criteria (all for no filters)'''
        cursor = self._connection.cursor()
        if sid=='' and tid == '' and searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty, comment FROM exercises ORDER BY zOrder'''
            cursor.execute(sqlTemplate)
        elif tid == '' and searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty, comment FROM exercises 
                    WHERE topicId IN (SELECT id FROM topics WHERE subjectId=?)
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (tid, ))
        elif sid == '' and searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty, comment FROM exercises 
                    WHERE topicId =?
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (tid, ))
        elif searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty, comment FROM exercises 
                    WHERE topicId=?
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (topic, ))
        else:
            sqlTemplate = '''SELECT id, title, topicId, difficulty, comment FROM exercises 
                    WHERE title LIKE '%?%' OR exercise LIKE '%?%' OR solution LIKE '%?%' OR comment LIKE '%?%'
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (searchword, searchword, searchword, searchword))
        tup = cursor.fetchall()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'title'     : t[1],
                        'topicId'   : t[2],
                        'difficulty': t[3],
                        'comment'   : t[4]
                    })
        return result
    
    def getExercise(self, exId):
        ''' returns an exersize from the database as dictionary '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM exercises WHERE id=?'''
        cursor.execute(sqlTemplate, (exId, ))
        tup = cursor.fetchone()
        if tup is None:
            return None
        result = {
                    'id'        : tup[0],
                    'title'     : tup[1],
                    'topicId'   : tup[2],
                    'difficulty': tup[3],
                    'exercise'  : tup[4],
                    'solution'  : tup[5],
                    'origin'    : tup[6],
                    'author'    : tup[7],
                    'year'      : tup[8],
                    'licenseId' : tup[9],
                    'comment'   : tup[10],
                    'zOrder'    : tup[11]
                }
        return result
    
    def getExercises(self, exes):
        ''' returns a list of exersizes from the database as dictionary '''
        cursor = self._connection.cursor()
        if (len(exes) == 1):
            sqlTemplate = '''SELECT * FROM exercises WHERE id={}'''.format(exes[0])
        else:
            sqlTemplate = '''SELECT * FROM exercises WHERE id IN {}'''.format(tuple(exes))
        cursor.execute(sqlTemplate)
        tup = cursor.fetchall()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'title'     : t[1],
                        'topicId'   : t[2],
                        'difficulty': t[3],
                        'exercise'  : t[4],
                        'solution'  : t[5],
                        'origin'    : t[6],
                        'author'    : t[7],
                        'year'      : t[8],
                        'licenseId' : t[9],
                        'comment'   : t[10],
                        'zOrder'    : t[11]
                    })
        return result
    
    def getSubjects(self):
        '''returns a list of all subjects as dict'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM subjects'''
        cursor.execute(sqlTemplate, )
        tup = cursor.fetchall()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'subject'   : t[1]
                    })
        return result
    
    def getSubjectId(self, subject):
        '''returns an id of a given subject'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM subjects WHERE subject=?'''
        cursor.execute(sqlTemplate, (subject, ))
        return cursor.fetchone()[0]
    
    def getTopic(self, tid):
        '''returns a topic (as dict) from an id'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM topics WHERE id=?'''
        cursor.execute(sqlTemplate, (tid, ))
        t = cursor.fetchone()
        if t is None:
            return None
        result = {
                    'id'        : t[0],
                    'subjectId' : t[1],
                    'topic'     : t[2],
                    'zOrder'    : t[3]
                }
        return result
    
    def getTopics(self, sid=''):
        '''returns a list of all topics (as dict) for a subject'''
        cursor = self._connection.cursor()
        if sid == '':
            sqlTemplate = '''
                    SELECT topics.id, subjectId, topic, zOrder, subject 
                    FROM topics JOIN subjects ON topics.subjectId=subjects.id'''
            cursor.execute(sqlTemplate)
        else:
            sqlTemplate = '''
                    SELECT topics.id, subjectId, topic, zOrder, subject 
                    FROM topics JOIN subjects ON topics.subjectId=subjects.id
                    WHERE subjectId=?'''
            cursor.execute(sqlTemplate, (sid, ))
        tup = cursor.fetchall()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'subjectId' : t[1],
                        'topic'     : t[2],
                        'zOrder'    : t[3],
                        'subject'   : t[4]
                    })
        return result
    
    def exerZMove(self, tid, eid, direction):
        '''move an exercise in zIndex up or down'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, zOrder FROM exercises WHERE topicId=? ORDER BY zOrder'''
        cursor.execute(sqlTemplate, (tid, ))
        exes = cursor.fetchall()
        for i in range(0,len(exes)):
            if exes[i][0] == eid:
                exe = exes[i]
                if i+direction >= 0:
                    try:
                        partner = exes[i+direction]
                    except IndexError:
                        return
                else:
                    return
        sqlTemplate = '''UPDATE exercises SET zOrder=? WHERE id=?'''
        cursor.execute(sqlTemplate, (partner[1], exe[0]))
        cursor.execute(sqlTemplate, (exe[1], partner[0]))
        self._connection.commit()
    
    def topicZIndexNormalize(self, tid):
        '''evenly spread zIndex for all exercises in a topic'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM exercises WHERE topicId=? ORDER BY zOrder'''
        cursor.execute(sqlTemplate, (tid, ))
        eids = cursor.fetchall()
        step = 10000 / (len(eids)+1)
        z = step
        sqlTemplate = '''UPDATE exercises SET zOrder=? WHERE id=?'''
        for eid in eids:
            cursor.execute(sqlTemplate, (z, eid[0]))
            z = z+step
        self._connection.commit()
    
    def getLicenses(self):
        '''returns a list of all licenses (as dict)'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM licenses'''
        cursor.execute(sqlTemplate, )
        tup = cursor.fetchall()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'name'      : t[1],
                        'license'   : t[2],
                        'url'       : t[3]
                    })
        return result
    

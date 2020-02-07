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
        cursor.execute(sqlTemplate, (e['title'][0], ))
        if cursor.fetchone():
            return 'exists'
        sqlTemplate = '''INSERT INTO exercises 
                (title, topicId, difficulty, exercise, solution, origin, author, year, licenseId, comment, zOrder) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        valuelist = (e['title'][0],
                    e['topicId'][0],
                    e['difficulty'][0],
                    e['exercise'][0],
                    e['solution'][0],
                    e['origin'][0],
                    e['author'][0],
                    e['year'][0],
                    e['licenseId'][0],
                    e['comment'][0],
                    e['zOrder'][0]
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        exerId = self.checkTitle(e['title'][0])
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
        valuelist = (e['title'][0],
                    e['topicId'][0],
                    e['difficulty'][0],
                    e['exercise'][0],
                    e['solution'][0],
                    e['origin'][0],
                    e['author'][0],
                    e['year'][0],
                    e['licenseId'][0],
                    e['comment'][0],
                    e['zOrder'][0],
                    e['eid'][0]
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
            result = e['eid'][0]
        except sqlite3.OperationalError as err:
            args = list(err.args)
            result = 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return result
    
    def getExerciseList(self, sid='', tid='', searchword=''):
        '''returns a List of exercises matching the filter criteria (all for no filters)'''
        cursor = self._connection.cursor()
        if sid=='' and tid == '' and searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty FROM exercises ORDER BY zOrder'''
            cursor.execute(sqlTemplate)
        elif tid == '' and searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty FROM exercises 
                    WHERE topicId IN (SELECT id FROM topics WHERE subjectId=?)
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (sid, ))
        elif searchword == '':
            sqlTemplate = '''SELECT id, title, topicId, difficulty FROM exercises 
                    WHERE topicId=?
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (topic, ))
        else:
            sqlTemplate = '''SELECT id, title, topicId, difficulty FROM exercises 
                    WHERE title LIKE '%?%' OR exercise LIKE '%?%' OR solution LIKE '%?%' OR comment LIKE '%?%'
                    ORDER BY zOrder'''
            cursor.execute(sqlTemplate, (searchword, searchword, searchword, searchword))
        return cursor.fetchall()
    
    def getExercise(self, exId):
        ''' returns an exersize from the database as dictionary '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM exercises WHERE id=?'''
        cursor.execute(sqlTemplate, (exId, ))
        result = cursor.fetchone()
        return result
    
    def getExercises(self, exes):
        ''' returns a list of exersizes from the database as dictionary '''
        cursor = self._connection.cursor()
        if (len(exes) == 1):
            sqlTemplate = '''SELECT * FROM exercises WHERE id={}'''.format(exes[0])
        else:
            sqlTemplate = '''SELECT * FROM exercises WHERE id IN {}'''.format(tuple(exes))
        cursor.execute(sqlTemplate)
        result = cursor.fetchall()
        return result
    
    def getSubjects(self):
        '''returns a list of all subjects'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM subjects'''
        cursor.execute(sqlTemplate, )
        return cursor.fetchall()
    
    def getSubjectId(self, subject):
        '''returns a list of all subjects'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM subjects WHERE subject=?'''
        cursor.execute(sqlTemplate, (subject, ))
        return cursor.fetchone()[0]
    
    def getTopics(self, sid=''):
        '''returns a list of all topics for a subject'''
        cursor = self._connection.cursor()
        if sid == '':
            sqlTemplate = '''SELECT * FROM topics'''
            cursor.execute(sqlTemplate)
        else:
            sqlTemplate = '''SELECT * FROM topics WHERE subjectId=?'''
            cursor.execute(sqlTemplate, (sid, ))
        return cursor.fetchall()
    
    def getLicenses(self):
        '''returns a list of all subjects'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM licenses'''
        cursor.execute(sqlTemplate, )
        return cursor.fetchall()
    

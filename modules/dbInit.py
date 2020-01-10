#!/usr/bin/python3
'''
Database-IO-file of TeXerBase - an Database Server for Exercises
'''

import sqlite3
import os
import yaml

batteriesFile = 'structure.yaml'

def checkTables(db):
    ''' makes sure default tables exist in the Database '''
    # subjects:
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER NOT NULL PRIMARY KEY,
            subject VARCHAR(256) NOT NULL
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create subjects table')
        err.args = tuple(args)
        raise
    # topics:
    sql_command = '''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER NOT NULL PRIMARY KEY,
            subjectId INTEGER NOT NULL,
            topic VARCHAR(256) NOT NULL,
            zOrder REAL,
            FOREIGN KEY (subjectId) REFERENCES subjects(id)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create topics table')
        err.args = tuple(args)
        raise
    # licenses:
    sql_command = '''
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            license TEXT,
            url VARCHAR(1024)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create licenses table')
        err.args = tuple(args)
        raise
    # exercises:
    sql_command = '''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER NOT NULL PRIMARY KEY,
            title VARCHAR(256) NOT NULL,
            topicId INTEGER,
            difficulty TINYINT,
            exercise TEXT,
            solution TEXT,
            origin VARCHAR(1024),
            author VARCHAR(256),
            year INTEGER,
            licenseId INTEGER,
            comment TEXT,
            zOrder REAL,
            FOREIGN KEY (topicId) REFERENCES topics(id),
            FOREIGN KEY (licenseId) REFERENCES licenses(id)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create exercises table')
        err.args = tuple(args)
        raise
    db._connection.commit()

def checkSubjects(db):
    ''' makes sure all subjects and topics are in the database '''
    cursor = db._connection.cursor()
    with open(batteriesFile) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for subject in data['subjects']:
            sqlTemplate = '''
                    SELECT id FROM subjects
                    WHERE subject=?'''
            sid = cursor.execute(sqlTemplate, (subject, )).fetchone()
            if not sid:
                sqlTemplate = '''INSERT INTO subjects(subject)
                        VALUES (?)'''
                cursor.execute(sqlTemplate, (subject, ))
                sqlTemplate = '''
                        SELECT id FROM subjects
                        WHERE subject=?'''
                sid = cursor.execute(sqlTemplate, (subject, )).fetchone()
            for topic in data['subjects'][subject]:
                sqlTemplate = '''
                        SELECT id FROM topics
                        WHERE (subjectId=? AND topic=?)'''
                tid = cursor.execute(sqlTemplate, (str(sid[0]), topic)).fetchone()
                if not tid:
                    sqlTemplate = '''INSERT INTO topics(subjectId, topic, zOrder)
                            VALUES (?, ?, ?)'''
                    cursor.execute(sqlTemplate, (str(sid[0]), topic, str(data['subjects'][subject].index(topic)+1)))
                else:
                    sqlTemplate = '''UPDATE topics
                            SET subjectId=?, topic=?, zOrder=?
                            WHERE id=?'''
                    cursor.execute(sqlTemplate, (str(sid[0]), topic, str(data['subjects'][subject].index(topic)+1), tid[0]))
    db._connection.commit()

def checkLicenses(db):
    ''' makes sure all licenses are in the database '''
    cursor = db._connection.cursor()
    with open(batteriesFile) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for lic in data['licenses']:
            sqlTemplate = '''
                    SELECT id FROM licenses
                    WHERE name=?'''
            lid = cursor.execute(sqlTemplate, (lic, )).fetchone()
            if not lid:
                sqlTemplate = '''INSERT INTO licenses (name, license, url)
                        VALUES (?, ?, ?)'''
                cursor.execute(sqlTemplate, (lic, data['licenses'][lic]['text'], data['licenses'][lic]['url']))
            else:
                sqlTemplate = '''UPDATE licenses
                        SET name=?, license=?, url=?
                        WHERE id=?'''
                valuelist = (lic,
                        data['licenses'][lic]['text'],
                        data['licenses'][lic]['url'],
                        str(lid[0]))
                cursor.execute(sqlTemplate, (valuelist))
    db._connection.commit()


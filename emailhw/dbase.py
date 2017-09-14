#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Initialize and manages the data base for the course.

The database should allow students to register, to submit homeworks,
and to get their grades and homework evaluations. I will also use the
database to log the incoming messages and the corresponding
action taken.

Student entity:

   student(ID,name,surname,email)

   ID and email must be unique. All messages from the same
   email will be considered coming from that student.

Homework entity:

   homework(ID,title,creation,deadline,required_attachments)

   ID must be unique, creation < deadline, and required_attachments
   must be something like Python,Sql,pdf.

Incoming Messages entity:

   message(Key,messageID,From,Date,commentary)

   This is to log incoming email messages. Both messageID and
   mailboxID should be unique, but they actually depend on the
   implementation. commentary describes which action has been taken
   when seeing this email

Sumbission relation:

   submit(student.RowID,homework.rowID,message.rowID,evaluation,filenames)

   each submission is logged. 'evaluation' can be N/A or a number, in
   order to represent submitted homeworks that haven't been
   graded yet.

"""

import sys
import sqlite3

from contextlib import AbstractContextManager


class dbase(AbstractContextManager):

    
    def __init__(self,filename=None):
            
        self.filename   = filename if filename is not None else ":memory:"
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.filename)
        return self
    
    def __exit__(self,*exc_details):
        self.connection.close()
        return False



    def initDB(self):
        """Create all the tables of database"""
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS
        student( 
        ID         text PRIMARY KEY NOT NULL,
        name       text NOT NULL,
        surname    text NOT NULL,
        email      text UNIQUE NOT NULL
        )""")

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS
        homework( 
        ID                    text PRIMARY KEY  NOT NULL,
        title                 text NOT NULL,
        creation              integer NOT NULL,
        deadline              integer NOT NULL,
        required_attachments  text,
        CHECK (creation < deadline)
        )""")

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS
        homework( 
        MessageID             text UNIQUE NOT NULL,
        sender                text NOT NULL,
        date                  integer NOT NULL,
        commentary            text DEFAULT NULL
        )""")
        
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS
        submit( 
        student    references student(rowid)  ON UPDATE CASCADE,
        homework   references homework(rowid) ON UPDATE CASCADE,
        message    references message(rowid)  ON UPDATE CASCADE,
        evaluation text DEFAULT NULL,
        filenames  text DEFAULT NULL
        )""")

    def newStudent(self,ID,name,surname,email):

        with self.connection as con:
            self.connection.execute('insert into student values(?,?,?,?)',
            (ID,name,surname,email))

    def logIncomingMessage(self,messageID,UID,Date,From,commentary):
        pass

    def newHomework(self,ID,title,deadline,required_attachments=[]):
        pass

    def allHomeworks(self):
        pass

    def newSubmission(self,homeworkID,studentID,messageID,mailboxID,filenames):
        pass

    def findStudentByEmail(self,emailAddress):
        with self.connection:
            con=self.connection.cursor()
            con.execute('select ID,name,surname,email from student where email=?',
                        (emailAddress,))
            students = con.fetchall()
            assert len(students) <= 1
            if len(students)==0:
                return None
            else:
                return {'ID'     : students[0][0],
                        'name'   :students[0][1],
                        'surname':students[0][2],
                        'email'  :students[0][3] }

    def findStudentByID(self,studentID):
        with self.connection:
            con=self.connection.cursor()
            con.execute('select ID,name,surname,email from student where ID=?',
                        (studentID,))
            students = con.fetchall()
            assert len(students) <= 1
            if len(students)==0:
                return None
            else:
                return {'ID'     :students[0][0],
                        'name'   :students[0][1],
                        'surname':students[0][2],
                        'email'  :students[0][3] }

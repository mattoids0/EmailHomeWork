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

   message(messageID,mailboxID,From,Date,commentary)

   This is to log incoming email messages. Both messageID and
   mailboxID should be unique, but they actually depend on the
   implementation. commentary describes which action has been taken
   when seeing this email

Sumbission relation:

   submit(studentID,homeworkID,messageID,mailboxID,evaluation,filenames)

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
        self.connection = sqlite3.connect(filename)

    
    def __exit__(self,*exc_details):
        self.connection.close()
        return False



    def initDB(self):
        """Create all the tables of database"""
        pass

    def newStudent(self,studentID,name,surname,email):
        pass

    def logIncomingMessage(self,messageID,UID,Date,From,commentary):
        pass

    def newHomework(self,homeworkID,title,deadline,required_attachments=[]):
        pass

    def allHomeworks(self):
        pass

    def newSubmission(self,homeworkID,studentID,messageID,mailboxID,filenames):
        pass

    def findStudentByEmail(self,email):
        pass

    def findStudentResults(self,studentID):
        pass

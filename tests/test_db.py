#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import unittest

from emailhw.dbase import dbase

class TestCommand(unittest.TestCase):
    """Test the basics of the db
    """

    def test_creation(self):

        with dbase() as D:
            D.initDB()

    def test_new_student(self):

        with dbase() as D:
            D.initDB()
            D.newStudent("12345",'Mickey','Mouse','topolino@topolinia.it')

            self.assertDictEqual(
                D.findStudentByEmail('topolino@topolinia.it'),
                {'ID':"12345",
                 'name':'Mickey',
                 'surname':'Mouse',
                 'email':'topolino@topolinia.it'}
            )
            
            self.assertDictEqual(
                D.findStudentByID('12345'),
                {'ID':"12345",
                 'name':'Mickey',
                 'surname':'Mouse',
                 'email':'topolino@topolinia.it'}
            )

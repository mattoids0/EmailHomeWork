#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import unittest

from emailhw import compile_command,CompilationFailed

class TestCommand(unittest.TestCase):
    """Test the commands and parsing
    """

    def test_compilation_no_command(self):
        with self.assertRaises(CompilationFailed) as cm:

            compile_command("""
            name : XXX
            surname : XXX
            """)
            
        self.assertEqual(len(cm.exception.get_errors()),1)

    def test_compilation_spaces(self):
        with self.assertRaises(CompilationFailed) as cm:

            compile_command("""
            sds  gadg dd 
            nac   me : XXX
            surname : XXX
            """)
            
        self.assertEqual(len(cm.exception.get_errors()),2)

    def test_compilation_missing(self):
        with self.assertRaises(CompilationFailed) as cm:

            compile_command("""
            ciao
              : XXX
              : XXX
            """)
            
        self.assertEqual(len(cm.exception.get_errors()),2)

    def test_compilation_double(self):
        with self.assertRaises(CompilationFailed) as cm:

            compile_command("""
            aaa
            ciao  : XXX
            aaa    :  ddfd XXX
            """)
            
        self.assertEqual(len(cm.exception.get_errors()),1)


if __name__ == '__main__':
    unittest.main()


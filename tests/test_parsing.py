#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Test messages parsing

"""

import unittest
from emailhw import compile_command





# example1 = """
# Salve professore, questa è la 

#   consegna

# del mio 

# homework:   AB1001

# spero che alla consegna sia magnanimo nella correzione.

# -- 
# Mario Rossi
# """

# with file_output_channel() as fout:

#     fout.send("Prova","pippo@topolinia.net","topolino@topolinia.net",
#               example1)

    

from emailhw import compile_command,CompilationFailed

class TestParsing(unittest.TestCase):
    """Test the commands and parsing
    """

    def setUp(self):
        self.command1 = compile_command(
            """
            command1
            field1 : xxxxx
            field2 : xxxxx
            """)

        self.command2 = compile_command(
            """
            command2
            """)
        

    
    def test_multiple_commands(self):
        text = """
        command1
        command2
        """        
        self.assertTrue(self.command1.detect(text))
        self.assertListEqual(self.command1.get_errors(),[])
        self.assertTrue(self.command2.detect(text))
        self.assertListEqual(self.command1.get_errors(),[])

    def test_wrong_commands(self):
        text = """
        command2
        """        
        self.assertFalse(self.command1.detect(text))
        self.assertIsNone(self.command1.parse(text))
        self.assertEqual(len(self.command1.get_errors()),3)
        
    def test_double_command(self):
        text = """
        command1
        command1
        field1 :xxxx
        field2 :xxxx
        """        
        self.assertTrue(self.command1.detect(text))
        self.assertNotEqual(self.command1.get_errors(),1)
        self.assertIsNone(self.command1.parse(text))
        self.assertNotEqual(self.command1.get_errors(),1)
    
        
    def test_missing_field(self):
        text = """
        command1
        field1 :xxxx
        """        
        self.assertTrue(self.command1.detect(text))
        self.assertIsNone(self.command1.parse(text))
        

    def test_good_entry(self):
        text = """
        
        snk jhjsah kh jhdkah jkah jdh jkah 

        command2

        dskh ajkdh jahj hjk ak
        """
        self.assertTrue(self.command2.detect(text))
        res = self.command2.parse(text)
        self.assertIsNotNone(res)
        self.assertDictEqual(res,dict())
        
    def test_good_entry2(self):
        text = """
        command1
        field1 :xx xx
        field2 :yy yy
        """        
        self.assertTrue(self.command1.detect(text))
        res = self.command1.parse(text)
        self.assertIsNotNone(res)
        self.assertDictEqual(res,{'field1':'xx xx','field2':'yy yy'})
        
    def test_additional_fields(self):
        text = """
        command1
        field1 :xx xx
        field2 :yy yy
        field3 :yy yy
        """        
        self.assertTrue(self.command1.detect(text))
        res = self.command1.parse(text)
        self.assertIsNotNone(res)
        self.assertDictEqual(res,{'field1':'xx xx','field2':'yy yy'})
        
    def test_double_field(self):
        text = """
        command1
        field1 :xx xx
        field2 :yy yy
        field2 :yy yy
        """        
        self.assertTrue(self.command1.detect(text))
        res = self.command1.parse(text)
        self.assertIsNone(res)
        self.assertEqual(len(self.command1.get_errors()),1)

    def test_empty_field(self):
        text = """
        command1
        field1 :xx xx
        field2 :
        """        
        self.assertTrue(self.command1.detect(text))
        res = self.command1.parse(text)
        self.assertIsNone(res)
        self.assertEqual(len(self.command1.get_errors()),1)
        
if __name__ == '__main__':
    unittest.main()


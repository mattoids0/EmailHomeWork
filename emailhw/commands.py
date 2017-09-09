#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Commands processing 

Commands to the system are issued by email. The template for each
command is transformed into a parsing function which verify and
validate messages.

Templates should follow some restriction, enforced by the command
compiler.
"""

import re
import sys

class CompilationFailed(ValueError):
    """Exception raised when a command compilation fails"""
    
    def __init__(self,text,error_list=None):
        
        self.text   = text
        self.errors = error_list

    def __str__(self):
        return self.text

    def get_errors(self):
        return self.errors
        

class Command:

    regexp_word_on_a_line = r"^[^\S\n\r]*(%s)[^\S\n\r]*$"
    regexp_inputfield_on_a_line = r"^" + r"[^\S\n\r]*" + r"(%s)" + r"[^\S\n\r]*" + r":(.+)$"

    def __init__(self,cmd_name,fields):
        self.cmd_name  = cmd_name
        self.fields    = fields
        self.cmd_re    = re.compile(self.regexp_word_on_a_line % cmd_name ,re.MULTILINE)
        self.fields_re = [re.compile(self.regexp_inputfield_on_a_line % field ,re.MULTILINE) for field in fields]
        self.last_errors = []
        
    def detect(self,msg):
        self.last_errors = []

        result = self.cmd_re.findall(msg)
        if len(result) == 0:
            return False

        if len(result) > 1:
            self.last_errors.append("Command <%s> occurs more than once"%self.cmd_name)

        return True
    
    def parse(self,msg):
        self.last_errors = []
    
        # this is to load detection error as well
        if not self.detect(msg):
            self.last_errors.append("Command <%s> missing"%self.cmd_name)
        
        values = dict()
        for field,regexp in zip(self.fields,self.fields_re):

            matches=regexp.findall(msg)
            
            if len(matches)==0:
                self.last_errors.append("Value for field <%s> missing" % field)
            elif len(matches)>1:
                self.last_errors.append("Multiple occurrence of field <%s>" % field)
            else:
                assert matches[0][0] == field
                values[field] = matches[0][1].strip()

        if len(self.last_errors)>0:
            return None
        
        else:
            return values
            
    def get_errors(self):
        return list(self.last_errors)
    
    def __str__(self):
        return self.cmd_name + "("+', '.join(self.fields) + ")" 
        

def compile_command(text):
    """Parse the template and produce a Command object
    """


    name     = None
    fields   = [  ]
    errors_lines = []

    has_spaces = re.compile(r'\s')

    for i,line in enumerate(text.splitlines(),start=1):

        if ':' in line:

            word = line.split(':')[0].strip()

            if len(word)==0:
                errors_lines.append((i,"Empty field name."))
            elif has_spaces.search(word):
                errors_lines.append((i,"No spaces allowed in field names."))
            else:
                fields.append(word)
        else:

            word = line.strip()

            if len(word)==0:
                continue
            elif has_spaces.search(word):
                errors_lines.append((i,"No spaces allowed inside a command."))
            elif name is not None:
                errors_lines.append((i,"Only one command is allowed."))
            else:
                name = word

    if name is None:            
        errors_lines.append((None,"No command found."))
    
    words = set([name] + fields)
    if len(words) < 1 + len(fields):
        errors_lines.append((None,"Repeated keywords in the template."))

    if len(errors_lines)>0:
        print("**Error parsing template**\n%s\n--------------------------" % text,file=sys.stderr)
        for l,e  in errors_lines:
            print("Line %s: %s" % (l or "END",e),file=sys.stderr)
        print('**************************',file=sys.stderr)
        sys.exit(1)
        
    return Command(name,fields)
    

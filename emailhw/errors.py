#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

def print_error(err_name,info=None):
    if info is None:
        print(errors[err_name],file=sys.stderr)
    else:
        print(errors[err_name].format(info),file=sys.stderr)
    
    

errors = {}

# Email I/O
errors['imap login']  = "[IMAP] Login failed. Check your credentials." 
errors['imap folder'] = "[IMAP] Unable to open folder. ({})"
errors['imap fetch']  = "[IMAP] During message fetch. {}" 
errors['smtp login']  = "[SMTP] Login failed. Check your credentials." 
errors['smtp send']   = "[SMTP] Impossible to send email {}" 

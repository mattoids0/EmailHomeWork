#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import keyring
import sys

import emailhw

from contextlib import contextmanager


def get_imap_password():
    return keyring.get_password(Config['imap server'],
                                Config['imap user'])
                                
def get_smtp_password():     
    return keyring.get_password(Config['smtp server'],
                                Config['smtp user'])


# Configuration file
Config = {

    # Homeworks are processed from email sent to a specific address in
    # a specific mailbox in an IMAP main server
    #
    'imap server'   : 'imap.gmail.com',
    'imap user'     : 'lauria.massimo@gmail.com',
    'imap mailbox'  : "progetti/INFOSEFA2017",
    #
    # The password may be a string or a function that return a string
    #
    'imap password' : get_imap_password,

    # Replies are send by mail as well
    #
    'sender'        : "Massimo Lauria <massimo.lauria@uniroma1.it>",
    'smtp server'   : 'smtp.gmail.com',
    'smtp user'     : 'lauria.massimo@gmail.com',
    #
    # The password may be a string or a function that return a string
    #
    'smtp password' : get_smtp_password,

    # Data storage
    #
    'storage path'  : "./infosefa2017-files/",
    'storage db'    : "./infosefa2017.db"   
}



# Default input channel for email
@contextmanager
def mail_input_channel():
    with emailhw.imap_input_channel(Config['imap server'],
                                    Config['imap user'],
                                    Config['imap password'] if isinstance(Config['imap password'],str) else Config['imap password'](),
                                    Config['imap mailbox']) as imap:
        yield imap
        

# Default mail output channel for email
@contextmanager
def mail_output_channel():
    with emailhw.smtp_output_channel(Config['smtp server'],
                                     Config['smtp user'],
                                     Config['smtp password'] if isinstance(Config['smtp password'],str) else Config['smtp password']()) as smtp:
        yield smtp
    

# Default commands
registration_cmd = emailhw.compile_command("""
iscrizione
nome      : <NOME> 
cognome   : <COGNOME>
matricola : <NUMERO DI MATRICOLA>
""")

submission_cmd = emailhw.compile_command("""
consegna
homework : <CODICE>
""")

status_cmd = emailhw.compile_command("""
situazione
""")

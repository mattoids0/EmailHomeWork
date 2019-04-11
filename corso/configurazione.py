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
ConfigurazioneCorso = {

    'email'         : "Matt Oids <matt_oids@securepost.one>",
    
    
    # Homeworks are processed from email sent to a specific address in
    # a specific mailbox in an IMAP main server
    #
    'imap server'   : 'mail.securepost.one',
    'imap user'     : 'matt_oids@securepost.one',
    'imap mailbox'  : "AWKw@rkf0x1996",
    #
    # The password may be a string or a function that return a string
    #
    'imap password' : get_imap_password,

    # Replies are send by mail as well
    #
    'smtp server'   : 'mail.securepost.one',
    'smtp user'     : 'matt_oids@securepost.one',
    #
    # The password may be a string or a function that return a string
    #
    'smtp password' : get_smtp_password,

    # Data storage
    #
    'storage path'  : "./infosefa2019-files/",
    'storage db'    : "./infosefa2019.db"   
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
    


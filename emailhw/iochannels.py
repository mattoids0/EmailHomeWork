#!/usr/bin/env python3
# -*- coding:utf-8 -*-



import sys
import smtplib
import imaplib
import mailbox
import socket

from contextlib import AbstractContextManager

from emailhw.errors   import print_error
from emailhw.messages import parse_rfc822,compose_email


#
# Base classes
#
class InputChannel():

    def __init__(self):
        raise RuntimeError("This is an abstract class. No implementation.")

    def __iter__(self):
        raise RuntimeError("This is an abstract class. No implementation.")

class OutputChannel():

    def __init__(self):
        raise RuntimeError("This is an abstract class. No implementation.")

    def send(self,Subject,From,To,body):
        raise RuntimeError("This is an abstract class. No implementation.")

#    
# Messages are loaded from the folder of an IMAP mailbox
#
class imap_input_channel(AbstractContextManager,InputChannel):

    def __init__(self,server,user,password,mailbox):
        self.server   = server
        self.user     = user
        self.password = password
        self.mailbox  = mailbox
        self.imapserver = None

    def __enter__(self):
        self.imapserver = imaplib.IMAP4_SSL(self.server)

        try:
            rv, data = self.imapserver.login(self.user, self.password)
        except imaplib.IMAP4.error:
            print_error('imap login')
            sys.exit(1)

        rv, data = self.imapserver.select(self.mailbox,readonly=True)
        if rv != 'OK':
            print_error('imap mailbox',info=self.mailbox)
            sys.exit(1)
        return self
    
    def __exit__(self,*exc_details):
        self.imapserver.close()
        self.imapserver.logout()

    def __iter__(self):
        
        rv, data = self.imapserver.search(None, "ALL")
        if rv != 'OK':
            return
        
        for num in data[0].split():
            try:

                rv, data = self.imapserver.fetch(num, '(RFC822)')

                if rv != 'OK':
                    raise imaplib.IMAP4.error("FETCH command error: return value %s" % rv)

                yield parse_rfc822(data[0][1])

            except imaplib.IMAP4.error as e:
                print_error('imap fetch', info=e)
                
#
# Messages are set out as email, through an SMTP server
#
class smtp_output_channel(AbstractContextManager,OutputChannel):

    def __init__(self,server,user,password):
        self.server   = server
        self.user     = user
        self.password = password
        self.smtpserver = None

    def __enter__(self):
        self.smtpserver = smtplib.SMTP(self.server,587)

        try:
            self.smtpserver.ehlo()
            self.smtpserver.starttls()
            self.smtpserver.ehlo()
            self.smtpserver.login(self.user, self.password)
        except smtplib.SMTPAuthenticationError:
            print_error('smtp login')
            sys.exit(1)
        return self
    
    def __exit__(self,*exc_details):
        self.smtpserver.quit()

    def send(self,Subject,From,To,body):
        msg = compose_email(Subject=Subject,From=From,To=To,body=body)
        try:
            self.smtpserver.send_message(msg)
        except socket.gaierror as e:
            print_error('smtp send',info=e)
            sys.exit(1)



#
# Messages are sent out to a file
#
class file_output_channel(AbstractContextManager,OutputChannel):
    
    def __init__(self,fout=sys.stdout):
        self.fout   = fout

    def __enter__(self):
        return self
    
    def __exit__(self,*exc_details):
        pass

    def send(self,Subject,From,To,body):
        print("Subject : %s\nFrom : %s\nTo : %s\n" % (Subject,From,To),file=self.fout)
        print(body,file=self.fout)

#
# Messages are placed on a Maildir mailbox
#
class mailbox_output_channel(AbstractContextManager,OutputChannel):

    def __init__(self,dirname,mailbox_class=mailbox.Maildir):
        self.mailbox   = mailbox_class(dirname,create=True)

    def __enter__(self):
        self.mailbox.lock()
        return self
    
    def __exit__(self,*exc_details):
        self.mailbox.unlock()
        return self

    def send(self,Subject,From,To,body):
        msg = compose_email(Subject=Subject,From=From,To=To,body=body)
        self.mailbox.add(msg)


#
# Messages are placed on a Maildir mailbox
#
class mailbox_input_channel(AbstractContextManager,OutputChannel):

    def __init__(self,dirname,mailbox_class=mailbox.Maildir):
        self.mailbox   = mailbox_class(dirname,create=False)

            
    def __enter__(self):
        self.mailbox.lock()
        return self
    
    def __exit__(self,*exc_details):
        self.mailbox.flush()
        self.mailbox.unlock()
        return self

    def __iter__(self):
        for k,msg in self.mailbox.iteritems():
            yield parse_rfc822(msg)
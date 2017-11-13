#!/usr/bin/env python3
# -*- coding:utf-8 -*-



import sys
import smtplib
import imaplib
import mailbox
import socket
import email.utils as emailutils

from contextlib import AbstractContextManager
from collections import deque

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

    def send(self,Subject,From,To,body,inReplyTo=None):
        raise RuntimeError("This is an abstract class. No implementation.")


    def reply(self,orig,From,body):
        self.send(
            Subject   = orig['Subject'],
            From      = From,
            To        = orig['From'],
            body      = body,
            inReplyTo = orig)


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
        return False

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
        return False

    def send(self,Subject,From,To,body,inReplyTo=None):
        email = compose_email(Subject=Subject,
                              From=From,
                              To=To,
                              body=body,
                              inReplyTo=inReplyTo)
        try:
            self.smtpserver.send_message(email)
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
        return False

    def send(self,Subject,From,To,body,inReplyTo=None):
        print("Subject : %s\nFrom : %s\nTo : %s" % (Subject,From,To),
              file=self.fout)
        try:
            print("Reply-To: %s\n" % inReplyTo['Message-ID'], file=self.fout)
        except:
            pass
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
        return False

    def send(self,Subject,From,To,body,inReplyTo=None):
        email = compose_email(Subject=Subject,
                              From=From,
                              To=To,
                              body=body,
                              inReplyTo=inReplyTo)
        self.mailbox.add(email)


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
        return False

    def __iter__(self):
        for k,msg in self.mailbox.iteritems():
            yield parse_rfc822(msg)


#
# Pipe IO channel
#
class pipe_io_channel(AbstractContextManager,OutputChannel,InputChannel):

    def __init__(self):

        self.msg_buffer =  deque()

    def __enter__(self):
        return self
    
    def __exit__(self,*exc_details):
        return False

    def send(self,Subject,From,To,body,inReplyTo=None):
        email = compose_email(Subject=Subject,
                              From=From,
                              To=To,
                              body=body,
                              inReplyTo=inReplyTo)

        local_representation = dict()
        local_representation['__body__'] = body

        for headerName,headerContent in email.items():
            local_representation[headerName]=headerContent
            
        self.msg_buffer.append(local_representation)

    def __iter__(self):

        try:
            yield self.msg_buffer.popleft()
        except IndexError:
            raise StopIteration
        
        

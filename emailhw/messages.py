#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Parse and compose messages into/from email

Input messages are parsed from `email.message.EmailMessage` into
a more manageable form. Output messages are prepared to be sent.

"""

import email
import email.message
import email.utils
import datetime


class MessageParseException(ValueError):
    pass

def my_read_header(header_string):
    """Get an header object from an header string

    Email header components must be encoded in ASCII. If the header
    contains some non ASCII characters then it is encoded.
    This function get the header string and produce a Header object,
    which is decoded to string automatically, when necessary.

    """
    text,enc = email.header.decode_header(header_string)[0]

    if isinstance(text,str):
        return text
    else:
        return text.decode(enc or 'utf-8')

def my_find_body_part(msg):
    """Find the main body of the message

    The message can contain a lot of nested multiparts and
    attachments. The body of the message is assumed to be the first
    'text/plain' part without a filename (in order to exclude
    'text/plain' attachments).
    """
    for part in msg.walk():
        if part.get_content_type() == 'text/plain' and part.get_filename() is None:
            return part
    raise MessageParseException("Cannot find the main text of the message.")


def my_iter_attachments(msg):
    """Find all file attachments

    These are assimed to be all parts of the message with an
    associated filename
    """
    yield from [part for part in msg.walk() if part.get_filename() is not None]

    # for part in msg.walk():
    #     if part.get_content_type() == 'text/plain' and part.get_filename() is None:
    #         return part
    # raise MessageParseException("Cannot find the main text of the message.")


def is_py_attachment(part):
    """Check if the part of the message is a PDF attachment
    """
    content_type = part.get_content_type()

    if content_type in ['application/x-python','text/x-python']:
        return True
    elif content_type == 'text/plain':
        filename = my_read_header(part.get_filename())
        extension = os.path.splitext(str(filename))[1]
        return extension.upper() == 'PY'
    else:
        return False
    
def is_pdf_attachment(part):
    """Check if the part of the message is a PDF attachment
    """
    content_type = part.get_content_type()

    if content_type in ['application/pdf','application/x-pdf']:
        return True
    elif content_type == 'application/octet-stream':
        filename = my_read_header(part.get_filename())
        extension = os.path.splitext(str(filename))[1]
        return extension.upper() == 'PDF'
    else:
        return False


def parse_rfc822(data):
    """Turn an rfc822 data frame into a more manageable format.

    It saves the info of PDF and PY attachments.
    """

    if not isinstance(data,email.message.Message):
        msg = email.message_from_bytes(data)
    else:
        msg = data

    received_message = {}

    def _set_header_safe(hdr_name):
        try:
            if msg[hdr_name] is not None:
                received_message[hdr_name]  = my_read_header(msg[hdr_name])
        except KeyError:
            pass
            
    # collect header (may produce None fields)
    _set_header_safe('Subject')
    _set_header_safe('From')
    _set_header_safe('To')
    _set_header_safe('Date')
    _set_header_safe('Message-ID')
    _set_header_safe('In-Reply-To')
    _set_header_safe('References')

    if msg['Date'] is not None:
        date_tuple = email.utils.parsedate_tz(msg['Date'])

        if date_tuple:
            received_message['Timestamp' ] = email.utils.mktime_tz(date_tuple)

            local_date = datetime.datetime.fromtimestamp(received_message['Timestamp'])
            received_message['Local-date'] = local_date.strftime("%a, %d %b %Y %H:%M:%S")
            
    # collect body
    body_part = my_find_body_part(msg)
    received_message['__body__']  = str(body_part.get_payload(decode=True),
                                    body_part.get_content_charset(),
                                    "ignore")

    # collect attachments
    received_message['__attachments__'] = []
    
    for part in my_iter_attachments(msg):

        filetype = None
        
        if is_pdf_attachment(part):

            filetype = 'pdf'
            
        elif is_py_attachment(part):

            filetype = 'py'

        if filetype is not None:
            
            filename = my_read_header(part.get_filename())
            filedata = part.get_payload(decode=True)
            received_message['__attachments__'].append((filetype,filename,filedata))

    if len(received_message['__attachments__']) == 0:
        del received_message['__attachments__']

    return received_message



def compose_email(Subject,From,To,body,inReplyTo=None):

    msg = email.message.EmailMessage()
    msg['Subject'] = Subject
    msg['From']    = From
    msg['To']      = To
    msg['Message-ID'] = email.utils.make_msgid()
    msg['Date']       = email.utils.formatdate(localtime=True)
    msg.set_content(body)

    if inReplyTo is None:
        return msg

    # Setup references
    try:
        if inReplyTo['References'] is not None:
            msg['References']   = inReplyTo['References']
    except KeyError:
        pass

    try:
        if inReplyTo['Message-ID'] is not None:
            msg['In-Reply-To']  = inReplyTo['Message-ID']
            msg['References']   += " " + inReplyTo['References']
    except KeyError:
        pass
        
    return msg


def print_message(msg):

    # Header
    for k in msg.keys():
        if k[:2] != "__":
            print("%s : %s" % (k,msg[k]))

    # Body length
    print("[...  %s  ...]" % len(msg['__body__']))

    # Attachments
    try:
        for ft,fn,fd in msg['__attachments__']:
            print("Attachment(%s) of %s bytes : %s " % (ft,len(fd),fn))
    except KeyError:
        pass

    print()

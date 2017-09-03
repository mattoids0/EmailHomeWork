#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import email
import socket
import shutil




from emailhw import mailbox_output_channel,mailbox_input_channel,print_message
from emailhw import mailbox_input_channel
from conf    import mail_input_channel




test_mailbox = "./mboxtest/"


#
# Send commands
#

print(">>>> Sending")

with mailbox_output_channel(test_mailbox) as outbox:


    outbox.send(
        Subject = "[INFOSEFA2017HW] Test message",
        From    = "Massimo Lauria <massimo.lauria@uniroma1.it>",
        To      = "Massimo Lauria <lauria.massimo@gmail.com>",
        body=
"""
iscrizione

nome : Massimo 
cognome : Lauria
matricola : 12345
""")

print(">>>> Receiving")

with mailbox_input_channel("./mboxtest/") as inbox:

    for i,msg in enumerate(inbox,start=1):

        
        # Print a report of the processed email
        print("***** Message %s *******"%i)
        print_message(msg)

    
# clear the mailbox at the end of the test
shutil.rmtree(test_mailbox)
        
with mail_input_channel() as inbox:
    for i,msg in enumerate(inbox,start=1):
        print("***** Message %s *******"%i)
        print_message(msg)

with mailbox_input_channel("~/Downloads/progetti.2017-sefa") as inbox:
    for i,msg in enumerate(inbox,start=1):
        print("***** Message %s *******"%i)
        print_message(msg)

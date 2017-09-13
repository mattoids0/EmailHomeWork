#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from emailhw import *


from corso import gestione_generale
from shutil import rmtree


input_mailbox = "./test.inbox"

            
if __name__ == '__main__':

    populate(input_mailbox)

    # Load messages from the input source
    with mailbox_input_channel(input_mailbox) as inbox, \
         file_output_channel() as outbox:        

        for msg in inbox:
            gestione_generale(msg,None,outbox)
    
    rmtree(input_mailbox)

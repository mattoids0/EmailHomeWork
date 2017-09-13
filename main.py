#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from emailhw import *


from corso import gestione_generale
from shutil import rmtree


input_mailbox = "./test.inbox"

def populate(mailbox):
    with mailbox_output_channel(mailbox) as mbox:
        mbox.send(
            Subject="Per favore vorrei iscrivermi",
            From="topolino@topolinia.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            Ciao, vorrei effettuare la mia iscrizione al sistema.

            iscrizione
            nome: Mickey
            cognome: Mouse
            matricola: 12345

            Grazie mille,
            """
        )

        mbox.send(
            Subject="Quack quack!",
            From="paperino@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            Quack! Iscrivetemi al sistema.

            iscrizione
            nome: Donald
            cognome: Duck
            matricola: 12345
            """
        )
        
        mbox.send(
            Subject="Quack quack quack e ancora quack!",
            From="paperino@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            Ancora non mi avete iscritto? Quaaaaaack!

            iscrizione
            nome: Donal
            cognome: Duck
            matricola: 12345
            """
        )

        mbox.send(
            Subject="Niente!",
            From="paperoga@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            iscrizione
            nome: Paperoga
            cognome: ...Duck?
            """
        )

        mbox.send(
            Subject="Per favore vorrei sapere la mia valutazione",
            From="topolino@topolinia.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            situazione

            matricola: 12345
            Grazie mille,
            """
        )

            
if __name__ == '__main__':

    populate(input_mailbox)

    # Load messages from the input source
    with mailbox_input_channel(input_mailbox) as inbox, \
         file_output_channel() as outbox:        

        for msg in inbox:
            gestione_generale(msg,None,outbox)
    
    rmtree(input_mailbox)

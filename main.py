#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from emailhw import *


from iscrizione    import comando  as iscrizione_cmd
from iscrizione    import gestione_comando as  gestione_iscrizione

from situazione    import comando  as situazione_cmd
from situazione    import gestione_comando as  gestione_situazione

from consegna      import comando  as consegna_cmd
from consegna      import gestione_comando as  gestione_consegna

from conf import Config
from shutil import rmtree


input_mailbox = "./test.inbox"


nocommand="""
Caro studente

il suo messaggio, ricevuto dall'indirizzo

{sender}

non è stato riconosciuto essere un comando valido. Forse hai inserito
più di un comando. Controlla che il messaggio sia stato formattato
correttamente secondo quando descritto nella pagina del corso

http://www.massimolauria.net/courses/infosefa2017/homework.html

In bocca al lupo per il corso!
-- 
Massimo Lauria
http://www.massimolauria.net

Università degli studi di Roma - La Sapienza
Dipartimento di Scienze Statistiche
Piazzale Aldo Moro, 5
00185 Roma, Italy
""" 



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

        
def main_logic(msg,DB,outbox):
    """Main logic of the program
    """
    # Understand command
    found_command = [
        cmd 
        for cmd in [consegna_cmd,iscrizione_cmd,situazione_cmd]
        if cmd.detect(msg['__body__'])
    ]

    if len(found_command)!=1:
        # Report error
        outbox.reply(msg,Config['email'],nocommand.format(sender=msg['From']))

    elif found_command[0] == iscrizione_cmd:

        gestione_iscrizione(msg,DB,outbox)
    
    elif found_command[0] == consegna_cmd:

        gestione_consegna(msg,DB,outbox)
        
    elif found_command[0] == situazione_cmd:

        gestione_situazione(msg,DB,outbox)
        
    else:
        raise RuntimeError('Reached a supposedly unreachable point in the code')

            

if __name__ == '__main__':

    populate(input_mailbox)

    # Load messages from the input source
    with mailbox_input_channel(input_mailbox) as inbox, \
         file_output_channel() as outbox:        

        for msg in inbox:
            main_logic(msg,None,outbox)
    
    rmtree(input_mailbox)

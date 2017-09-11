#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from emailhw import *


from iscrizione    import comando  as iscrizione_cmd
from iscrizione    import gestione_comando as  gestione_iscrizione

from situazione    import comando  as situazione_cmd
from situazione    import gestione_comando as  gestione_situazione

from consegna      import comando  as consegna_cmd

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



def populate():
    with mailbox_output_channel(input_mailbox) as mbox:
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
            Subject="Tutto o niente!",
            From="paperoga@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            iscrizione
            nome: Paperoga
            cognome: ...Duck?
            matricola: 12345

            consegna
            homework: njahjkdf

            situazione
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
            Subject="Per favore vorrei iscrivermi",
            From="topolino@topolinia.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            situazione

            matricola: 12345
            Grazie mille,
            """
        )

        
def main():
    """Main logic of the program
    """
    
    # Load messages from the input source
    with mailbox_input_channel(input_mailbox) as inbox, \
         file_output_channel() as outbox:        


        def _reply(orig,reply_text):
            outbox.send(
                Subject = "Re: {}".format(orig['Subject']),
                From = Config['email'],
                To = orig['From'],
                body = reply_text,
                inReplyTo = orig
            )

            
            
        for msg in inbox:

            print("/---------------------------------------\\")
            print("Processing message: {}".format(msg['Message-ID']))
            print("Subject: {}".format(msg['Subject']))
            print("From: {}".format(msg['From']))
            print("To: {}".format(msg['To']))
            print("|---------------------------------------|")
            
            # Understand command
            found_command = [
                cmd 
                for cmd in [consegna_cmd,iscrizione_cmd,situazione_cmd]
                if cmd.detect(msg['__body__'])
            ]

            if len(found_command)!=1:
                # Report error
                outbox.reply(msg,Config['email'],nocommand.format(sender=msg['From']))

            # Iscrizione 
            elif found_command[0] == iscrizione_cmd:

                gestione_iscrizione(None,inbox,outbox,msg)
            
            elif found_command[0] == consegna_cmd:
                print('Consegna')
                
            elif found_command[0] == situazione_cmd:

                gestione_situazione(None,inbox,outbox,msg)
                
            else:
                raise RuntimeError('Reached a supposedly unreachable point in the code')

            

if __name__ == '__main__':
    populate()
    main()
    rmtree(input_mailbox)

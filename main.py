#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from emailhw import *

from messaggi import *
from conf import registration_cmd,submission_cmd,status_cmd
from conf import Config


input_mailbox = "./test.inbox"
input_mailbox = "./test.outbox"

def populate():
    with mailbox_output_channel("./test.inbox") as mbox:
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
            nome: Donal
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
            nome: Donal
            cognome: Duck
            matricola: 12345

            consegna
            homework: njahjkdf

            situazione
            """
        )


def main():
    """Main logic of the program
    """
    
    # Load messages from the input source
    with mailbox_input_channel("./test.inbox") as inbox, \
         file_output_channel() as outbox:        


        def _reply(orig,reply_text):
            outbox.send(
                Subject = 'Re: {}'.format(orig['Subject']),
                From = Config['sender'],
                To = orig['From'],
                body = reply_text,
                inReplyTo = orig
            )

            
            
        for msg in inbox:

            print("Processing message: {}",msg['Message-ID'])
            print("Subject: {}",msg['Subject'])
            print("From: {}",msg['From'])
            print("To: {}",msg['To'])
            
            # Understand command
            found_command = [
                cmd 
                for cmd in [registration_cmd,submission_cmd,status_cmd]
                if cmd.detect(msg['__body__'])
            ]

            if len(found_command)!=1:
                # Report error
                _reply(msg,messaggi['quale comando?'].format(
                    registration_email=msg['From']))
                continue

            # Registration 
            if found_command[0] == registration_cmd:

                data = registration_cmd.parse(msg['__body__'])

                if data is None:
                    # Registration error
                    _reply(msg,messaggi['registrazione ERRORE'].format(
                        registration_email=msg['From'],
                        registration_error='\n'.join(data.get_errors())))                
                else:
                    # Registration OK
                    _reply(msg,messaggi['registrazione ERRORE'].format(
                        registration_email=msg['From'],
                        registration_nome=data['nome'],
                        registration_cognome=data['cognome'],
                        registration_matricola=data['matricola']
                    ))                
            else:
                print('Incomplete')


if __name__ == '__main__':
    populate()
    main()

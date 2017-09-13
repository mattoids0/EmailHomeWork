#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from emailhw import *


from corso.iscrizione    import comando  as iscrizione_cmd
from corso.iscrizione    import gestione_comando as  gestione_iscrizione

from corso.situazione    import comando  as situazione_cmd
from corso.situazione    import gestione_comando as  gestione_situazione

from corso.consegna      import comando  as consegna_cmd
from corso.consegna      import gestione_comando as  gestione_consegna

from corso.configurazione import ConfigurazioneCorso

messaggi=dict()
messaggi['ERRORE']="""
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

        
def gestione_generale(msg,DB,outbox):
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
        outbox.reply(msg,
                     ConfigurazioneCorso['email'],
                     messaggi['ERRORE'].format(sender=clean_address(msg['From'])))

    elif found_command[0] == iscrizione_cmd:

        gestione_iscrizione(msg,DB,outbox)
    
    elif found_command[0] == consegna_cmd:

        gestione_consegna(msg,DB,outbox)
        
    elif found_command[0] == situazione_cmd:

        gestione_situazione(msg,DB,outbox)
        
    else:
        raise RuntimeError('Reached a supposedly unreachable point in the code')


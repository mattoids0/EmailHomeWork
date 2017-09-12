#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from emailhw import compile_command
from conf import Config

comando = compile_command("""
situazione
""")



messaggi=dict()


messaggi['OK']="""
Ciao {nome}, 

ti invio tutte le informazioni riguardanti lo stato dei tuoi esercizi.

{nome} {cognome}
Matricola: {matricola}

<REPORT PLACEHOLDER>

A presto,
-- 
Massimo Lauria
http://www.massimolauria.net

Università degli studi di Roma - La Sapienza
Dipartimento di Scienze Statistiche
Piazzale Aldo Moro, 5
00185 Roma, Italy
"""



def gestione_comando(msg,DB,outbox):
    """
    Gestisci i comandi di richiesta della situazione.

    Parameters
    ----------
    DB : database
    
    inbox : InputChannel

    outbox : OutputChannel
    
    msg : email.messages.EmailMessage

    Returns
    -------
    None
    """
    
    data = comando.parse(msg['__body__'])

    if data is None:
        raise RuntimeError('Reached a supposedly unreachable point in the code')

    else:
        # Registration OK
        outbox.reply(msg,
                     Config['email'],
                     messaggi['OK'])

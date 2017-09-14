#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from emailhw import compile_command,clean_address

from corso.configurazione import ConfigurazioneCorso

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

messaggi['ERRORE']="""
Caro studente,

il tentativo di registrazione ricevuto dall'indirizzo

{email}

è fallito. Il tuo indirizzo email non corrisponde a nessuno studente.
Sei sicuro di esserti iscritto al sistema?

In bocca al lupo per il corso!
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

    sender = clean_address(msg['From'])
    student = DB.findStudentByEmail(sender)

    if student is None:
        outbox.reply(msg,
                     ConfigurazioneCorso['email'],
                     messaggi['ERRORE'].format(email=sender))
    else:
        outbox.reply(msg,
                     ConfigurazioneCorso['email'],
                     messaggi['OK'].format(nome=student['name'],
                                           cognome=student['surname'],
                                           matricola=student['ID']))

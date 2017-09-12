#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from emailhw import compile_command
from conf import Config

comando = compile_command("""
iscrizione
nome      : <NOME> 
cognome   : <COGNOME>
matricola : <NUMERO DI MATRICOLA>
""")



messaggi=dict()


messaggi['OK']="""
Grazie per la registrazione, {nome}. 

D'ora in poi potrai inviare i tuoi compiti via email. Quando lo fai
ricordati di utilizzare esclusivamente l'indirizzo di posta
elettronica

{email}

che è l'indirizzo corrispondente al nominativo

{nome} {cognome}
Matricola: {matricola}

In bocca al lupo per il corso!
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

è fallito. Il problema è 

{error_list}

É sufficiente (e necessario) registrarsi una sola volta,
includendo le informazioni necessarie. Ad esempio

 nome : Massimo
 cognome : Lauria
 matricola : 123456789

Controlla che il messaggio sia stato formattato correttamente secondo
quando descritto nella pagina del corso

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


def gestione_comando(msg,DB,outbox):
    """
    Gestisci i comandi di iscrizione.

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
        # Registration error
        outbox.reply(msg,
                     Config['email'],
                     messaggi['ERRORE'].format(
                         email=msg['From'],
                         error_list='\n'.join(comando.get_errors())))                
    else:
        # Registration OK
        outbox.reply(msg,
                     Config['email'],
                     messaggi['OK'].format(
                         email=msg['From'],
                         nome=data['nome'],
                         cognome=data['cognome'],
                         matricola=data['matricola']
        ))

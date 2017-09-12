#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import emailhw


comando = emailhw.compile_command("""
consegna
homework : <CODICE>
""")


messaggi=dict()


messaggi['OK']="""
Grazie  {nome}. 

per aver consegnato il compito {codice}

Il compito verrà corretto nei prossimi giorni e il risultato
farà parte della tua situazione.

In bocca al lupo per i prossimi compiti!
-- 
Massimo Lauria
http://www.massimolauria.net

Università degli studi di Roma - La Sapienza
Dipartimento di Scienze Statistiche
Piazzale Aldo Moro, 5
00185 Roma, Italy
"""

messaggi['ERRORE']="""
Grazie  {nome},

ma sembra che si sia un problema nel compito consegnato. Controlla che
il messaggio sia stato formattato correttamente secondo quando
descritto nella pagina del corso

http://www.massimolauria.net/courses/infosefa2017/homework.html

In particolare assicurati che in allegato ci sia un solo file, del
formato richiesto dall'esercizio.

Errori nell'email di consegna:

{error_list}

Riprova a consegnare!
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
    Gestisci i comandi di consegna.

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
        outbox.reply(msg,
                     Config['email'],
                     messaggi['ERRORE'].format(
                         email=msg['From'],
                         error_list='\n'.join(comando.get_errors())))                
    else:
        outbox.reply(msg,
                     Config['email'],
                     messaggi['OK'].format(
                         email=msg['From'],
                         nome=data['nome'],
                         cognome=data['cognome'],
                         matricola=data['matricola']
        ))

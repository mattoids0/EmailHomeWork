#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from emailhw import compile_command,clean_address
from corso.configurazione import ConfigurazioneCorso

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

messaggi['DOUBLE']="""
Caro studente,

il tentativo di registrazione ricevuto dall'indirizzo

{email}

è fallito. Esite già uno studente iscritto con questo indirizzo.
Se questo studente non sei tu, e questo è il tuo indirizzo di posta
elettronica ti prego di contattarmi immediatamente.

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

    # Test that matricola is well formatted

    
    # Message is not well formatted
    if data is None:
        outbox.reply(msg,
                     ConfigurazioneCorso['email'],
                     messaggi['ERRORE'].format(
                         email=clean_address(msg['From']),
                         error_list='\n'.join(comando.get_errors())))
        return


    
    # Student already registered
    entry = DB.findStudentByEmail(clean_address(msg['From']))
    if entry is not None:
        outbox.reply(msg,
                     ConfigurazioneCorso['email'],
                     messaggi['DOUBLE'].format(
                         email=clean_address(msg['From'])))
        return

    
    # Registration OK
    DB.newStudent(ID=data['matricola'],
                  name=data['nome'],
                  surname=data['cognome'],
                  email=clean_address(msg['From']))
    # query as a double check
    entry = DB.findStudentByID(data['matricola'])
    
    outbox.reply(msg,
                     ConfigurazioneCorso['email'],
                     messaggi['OK'].format(
                         email=entry['email'],
                         nome=entry['name'],
                         cognome=entry['surname'],
                         matricola=entry['ID']
        ))

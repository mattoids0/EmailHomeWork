#!/usr/bin/env python3
# -*- coding:utf-8 -*-


messaggi=dict()



messaggi['quale comando?']="""
Caro studente

il suo messaggio, ricevuto dall'indirizzo

{registration_email}

non è stato riconosciuto essere un comando valido. Controlla che il
messaggio sia stato formattato correttamente secondo quando descritto 
nella pagina del corso

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


messaggi['registrazione OK']="""
Grazie per la registrazione, {registration_nome}. 

D'ora in poi potrai inviare i tuoi compiti via email. Quando lo fai
ricordati di utilizzare esclusivamente l'indirizzo di posta
elettronica

{registration_email}

che è l'indirizzo corrispondente al nominativo

{registration_nome} {registration_cognome}
Matricola: {registration_matricola}

In bocca al lupo per il corso!
-- 
Massimo Lauria
http://www.massimolauria.net

Università degli studi di Roma - La Sapienza
Dipartimento di Scienze Statistiche
Piazzale Aldo Moro, 5
00185 Roma, Italy
"""

messaggi['registrazione ERRORE']="""
Caro studente,

il tentativo di registrazione ricevuto dall'indirizzo

{registration_email}

è fallito. Il problema è 

{registration_error}

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

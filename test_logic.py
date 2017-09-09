#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Email processing

Commands to the system are issued by email. The template for each
command is transformed into a parsing function which verify and
validate the message.
"""

from emailhw import *



registration = compile_command(
    """
    iscrizione
    nome : xxxxx
    cognome : xxxxx
    matricola : xxxxxx
    """)

submission   = compile_command(
    """
    consegna
    homework : xxxxx
    """)

report       = compile_command(
    """
    situazione
    """)


example1 = """
Salve professore, questa è la 

  consegna

del mio 

homework:   AB1001

spero che alla consegna sia magnanimo nella correzione.

-- 
Mario Rossi
"""

with file_output_channel() as fout:

    fout.send("Prova","pippo@topolinia.net","topolino@topolinia.net",
              example1)

    

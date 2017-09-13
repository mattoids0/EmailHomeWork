#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import unittest

from tests.test_gestione import TestGestione

from corso import gestione_situazione
from corso.situazione import messaggi

class TestIscrizione(TestGestione):
    """Testa la gestione delle iscrizioni"""


    def test_situazione(self):

        text=self.getAnswerText(
            Subject="Per favore vorrei sapere la mia valutazione",
            From="topolino@topolinia.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            situazione

            matricola: 12345
            Grazie mille,
            """,
            DB=None,manager=gestione_situazione)

        self.assertEqual(text,messaggi['OK'].format(nome="Mickey",cognome='Mouse'))
 
        text=self.getAnswerText(
            Subject="Per favore vorrei sapere la mia valutazione",
            From="topolino@topolinia.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            situazione
            """,
            DB=None,manager=gestione_situazione)

        self.assertEqual(text,messaggi['OK'].format(nome="Mickey",cognome='Mouse'))
 

if __name__ == '__main__':
    unittest.main()


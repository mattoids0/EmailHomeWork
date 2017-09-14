#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import unittest

from tests.test_gestione import TestGestione

from corso import gestione_situazione,gestione_iscrizione
from corso.situazione import messaggi
from emailhw.dbase import dbase

class TestSituazione(TestGestione):
    """Testa la richiesta della situazione"""


    def test_situazione(self):

        with dbase() as localD:
            localD.initDB()

            text=self.getAnswerText(
                Subject="Per favore vorrei sapere la mia valutazione",
                From="topolino@topolinia.it",
                To="massimo.lauria@uniroma1.it",
                body="""
            
                situazione

                matricola: 12345
                Grazie mille,
                """,
                DB=localD,manager=gestione_situazione)

            self.assertEqual(text,messaggi['ERRORE'].format(
                email="topolino@topolinia.it"))


            localD.newStudent(ID='12345',
                              name='Mickey',
                              surname='Mouse',
                              email='topolino@topolinia.it')

            text=self.getAnswerText(
                Subject="Per favore vorrei sapere la mia valutazione",
                From="topolino@topolinia.it",
                To="massimo.lauria@uniroma1.it",
                body="""
            
                situazione

                matricola: 12345
                Grazie mille,
                """,
                DB=localD,manager=gestione_situazione)

            self.assertEqual(text,messaggi['OK'].format(nome="Mickey",
                                                        cognome='Mouse',
                                                        matricola='12345'))
 
            text=self.getAnswerText(
                Subject="Per favore vorrei sapere la mia valutazione",
                From="topolino@topolinia.it",
                To="massimo.lauria@uniroma1.it",
                body="""
                
                situazione
                """,
                DB=localD,manager=gestione_situazione)

            self.assertEqual(text,messaggi['OK'].format(nome="Mickey",
                                                        cognome='Mouse',
                                                        matricola='12345'))
 

if __name__ == '__main__':
    unittest.main()


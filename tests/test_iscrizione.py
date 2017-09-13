#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import unittest

from tests.test_gestione import TestGestione

from corso import gestione_iscrizione
from corso.iscrizione import messaggi




class TestIscrizione(TestGestione):
    """Testa la gestione delle iscrizioni"""


    def test_iscrizione_corretta(self):

        text=self.getAnswerText(
            Subject="Per favore vorrei iscrivermi",
            From="topolino@topolinia.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            Ciao, vorrei effettuare la mia iscrizione al sistema.

            iscrizione
            nome: Mickey
            cognome: Mouse
            matricola: 12345

            Grazie mille,
            """,
            DB=None,manager=gestione_iscrizione)

        self.assertEqual(text,messaggi['OK'].format(email='topolino@topolinia.it',
                                                    nome="Mickey",
                                                    cognome='Mouse',
                                                    matricola='12345'))
 

    def test_iscrizione_incompleta(self):
        text=self.getAnswerText(
            Subject="Niente!",
            From="paperoga@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            iscrizione
            nome: Paperoga
            cognome: ...Duck?
            """,
            DB=None,manager=gestione_iscrizione)

        self.assertEqual(text,messaggi['ERRORE'].format(email="paperoga@paperopoli.it",error_list='Manca il campo <matricola>.'))
 
    def test_iscrizione_doppia(self):

        text = self.getAnswerText(
            Subject="Quack quack!",
            From="paperino@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            Quack! Iscrivetemi al sistema.

            iscrizione
            nome: Donald
            cognome: Duck
            matricola: 12345
            """,
            DB=None,manager=gestione_iscrizione)
        self.assertEqual(text,messaggi['OK'].format(email="paperino@paperopoli.it",nome='Donald',cognome='Duck',matricola='12345'))

        text = self.getAnswerText(
            Subject="Quack quack quack e ancora quack!",
            From="paperino@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            Ancora non mi avete iscritto? Quaaaaaack!

            iscrizione
            nome: Donal
            cognome: Duck
            matricola: 12345
            """,
            DB=None,manager=gestione_iscrizione)
        
        self.assertEqual(text,messaggi['ERRORE'])

if __name__ == '__main__':
    unittest.main()


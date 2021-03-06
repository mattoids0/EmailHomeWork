#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import unittest

from emailhw.iochannels import pipe_io_channel

from corso.generale import gestione_generale,messaggi


class TestGestione(unittest.TestCase):
    """Testa la gestione dei messaggi"""

    def getAnswer(self,Subject,From,To,body,DB,manager=None):

        if manager is None:
            return None
        
        with pipe_io_channel() as inbox, pipe_io_channel() as outbox:

            inbox.send(Subject = Subject, From = From, To = To, body = body)

            for msg in inbox:

                manager(msg,DB,outbox)

            outputs = list(outbox)

            self.assertEqual(len(outputs),1)
            self.assertEqual(outputs[0]['Subject'],Subject)
            self.assertEqual(outputs[0]['To'],From)
            return outputs[0]

    def getAnswerText(self,Subject,From,To,body,DB,manager=None):
        self.maxDiff = None
        msg = self.getAnswer(Subject,From,To,body,DB,manager)
        return msg['__body__']

    def getAttachmentCount(self,Subject,From,To,body,DB,manager=None):

        msg = self.getAnswer(Subject,From,To,body,DB,manager)

        try:
            count = dict()
            for (ftype,_,_) in msg['__attachment__']:
                count[ftype] = count.setdefault(ftype,0) + 1
            return count
        except KeyError:
            return {}

        
class TestCommandDetection(TestGestione):

    def test_nocommand(self):

        text=self.getAnswerText(
            Subject="Tutto o niente!",
            From="paperoga@paperopoli.it",
            To="massimo.lauria@uniroma1.it",
            body="""
            
            iscrizione
            nome: Paperoga
            cognome: ...Duck?
            matricola: 12345

            consegna
            homework: njahjkdf

            situazione
            """,
            DB=None,manager=gestione_generale)

        self.assertEqual(text,messaggi['ERRORE'].format(sender="paperoga@paperopoli.it"))
        



if __name__ == '__main__':
    unittest.main()


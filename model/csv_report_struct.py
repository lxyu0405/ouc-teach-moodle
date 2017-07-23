# -*- coding: utf8 -*-


class CSVReportStruct:
    name = u''
    title = u''
    sents_cnt = 0
    plag_cnt = 0
    plag_cent = 0.0
    peer_grade = 0.0


    def __init__(self):
        self.name = u''
        self.title = u''
        self.sents_cnt = 0
        self.plag_cnt = 0
        self.plag_cent = 0.0
        self.peer_grade = 0.0
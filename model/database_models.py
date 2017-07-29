# -*- coding: utf8 -*-

class MdlWorkshopPlagReport():
    author_id = 0
    author_name = ''
    title = ''
    sentence_cnt = 0
    plg_cnt = 0
    plg_cent = 0.0
    ws_grading = 0.0
    def __init__(self):
        self.author_id = 0
        self.author_name = ''
        self.title = ''
        self.sentence_cnt = 0
        self.plg_cnt = 0
        self.plg_cent = 0.0
        self.ws_grading = 0.0

class MdlWorkshopPlag:
    plag_id = 0
    author_id = 0
    sentence_id = 0
    sentence_content = ''
    ref1_content = ''
    ref1_similarity = 0.0
    ref2_content = ''
    ref2_similarity = 0.0
    def __init__(self):
        self.plag_id = 0
        self.author_id = 0
        self.sentence_id = 0
        self.sentence_content = ''
        self.ref1_content = ''
        self.ref1_similarity = 0.0
        self.ref2_content = ''
        self.ref2_similarity = 0.0




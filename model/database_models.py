# -*- coding: utf8 -*-

class MdlWorkshopPlagReport():
    # 学生用户id
    author_id = 0
    # 学生姓名
    author_name = ''
    # 学生文章标题
    title = ''
    # 学生文章中有效句子数量
    sentence_cnt = 0
    # 学生文章中可疑抄袭句子数量
    plg_cnt = 0
    # 学生文章中可疑抄袭句子比例
    plg_cent = 0.0
    # 该学生在互评阶段的成绩
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
    # PK, AI
    plag_id = 0
    # 学生用户id
    author_id = 0
    # 学生句子id
    sentence_id = 0
    # 学生句子内容
    sentence_content = ''
    # 与参考文献1中最相似的句子
    ref1_content = ''
    # 与参考文献1中最相似句子的相似度
    ref1_similarity = 0.0
    # 与参考文献2中最相似的句子
    ref2_content = ''
    # 与参考文献2中最相似句子的相似度
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




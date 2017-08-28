# -*- coding: utf8 -*-
import ConfigParser
import sys
import time

import mysql.connector

from model import database_models, stu_asgn_info
from utils import char_tools, lcs

reload(sys)
sys.setdefaultencoding('utf-8')

# 读取配置文件中的配置
CONFIG = ConfigParser.ConfigParser()
# config file path
CONFIG.read('config.conf')
# project information
SLN_DIR = CONFIG.get('project', 'dir')
SLN_NAME = CONFIG.get('project', 'name')
SLN_AUTHOR = CONFIG.get('project', 'author')
# database information
MOODLE_DB_USERNAME = CONFIG.get('moodle_db', 'username')
MOODLE_DE_PWD = CONFIG.get('moodle_db', 'password')
MOODLE_DB_HOST = CONFIG.get('moodle_db', 'db_host')
MOODLE_DB_PORT = CONFIG.get('moodle_db', 'db_port')
MOODLE_DB_DBNAME = CONFIG.get('moodle_db', 'db_name')
# references infomation
REF1_TITLE = CONFIG.get('references', 'ref1_title')
REF1_DIR = CONFIG.get('references', 'ref1_dir')
REF2_TITLE = CONFIG.get('references', 'ref2_title')
REF2_DIR = CONFIG.get('references', 'ref2_dir')


# 计算函数执行时间
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f s' % (f.func_name, time2-time1)
        return ret
    return wrap

# 全局变量：裁定抄袭阈值
PLAG_THRESHOLD = 0.7

# 学生作业信息列表
STU_ASGN_LIST = []

# 参考文献1中的句子
REF1_SENTS = []

# 参考文献2中的句子
REF2_SENTS = []

# 参考文献的标题
# 用于去除引用的影响
REF_TITLE = []

# 整理成报告列表
REPORT_LIST = []


# 整理参考文献数据
@timing
def prepare_ref_data():
    # prepare sentences data for ref1
    for line in open(SLN_DIR + REF1_DIR):
        for sent in lcs.PlagDetect.cut_sentence(line):
            this_sent = char_tools.CharTools.clean_spaces(sent)
            if len(this_sent) > 6:
                REF1_SENTS.append(this_sent)
    for sent in lcs.PlagDetect.cut_sentence(REF1_TITLE):
        REF_TITLE.append(sent)

    # prepare sentences data for ref2
    for line in open(SLN_DIR + REF2_DIR):
        for sent in lcs.PlagDetect.cut_sentence(line):
            this_sent = char_tools.CharTools.clean_spaces(sent)
            if len(this_sent) > 6:
                REF2_SENTS.append(this_sent)
    for sent in lcs.PlagDetect.cut_sentence(REF2_TITLE):
        REF_TITLE.append(sent)

# 从db中读取学生作业详情
@timing
def stu_assgn_data_from_db(db_list):
    for item in db_list:
        stu_asgn_item = stu_asgn_info.StuAsgnInfo()
        stu_asgn_item.author_id = item[0]
        stu_asgn_item.last_name = item[1]
        stu_asgn_item.first_name = item[2]
        stu_asgn_item.username = item[3]
        stu_asgn_item.email = item[4]
        stu_asgn_item.title = item[5]
        # clean the content
        # remove html tags e.g. '<h1></h1>'
        # remove spaces, meaningless symbol, nbsp
        stu_asgn_item.content = char_tools.CharTools.clean_nbsp(char_tools.CharTools.clean_meaningless_symbol(
            char_tools.CharTools.clean_spaces(char_tools.CharTools.clean_html_tags(item[6]))))
        stu_asgn_item.grade = item[7]
        STU_ASGN_LIST.append(stu_asgn_item)

# 学生作业文本切割成句子
@timing
def stu_sents_from_content(str_content):
    stu_sent_list = []
    for sent in lcs.PlagDetect.cut_sentence(str_content):
        for ref_title in REF_TITLE:
            # remove reference (title) sentence in student assignment
            if ref_title not in sent and len(sent) > 6:
                stu_sent_list.append(sent)
                break
    return stu_sent_list

# 整理成报告形式
@timing
def stu_plag_report(author_id, stu_sents, ref1_sents, ref2_sents):
    stu_plag_list = []
    cnt = 1
    for sent in stu_sents:
        stu_plag = database_models.MdlWorkshopPlag()
        stu_plag.author_id = author_id
        stu_plag.sentence_id = cnt
        cnt += 1
        stu_plag.sentence_content = sent
        for ref1_sent in ref1_sents:
            similarity = len(lcs.PlagDetect.rmmlsslst(lcs.PlagDetect.lcs(sent, ref1_sent))) / float(len(lcs.PlagDetect.rmmlsslst(sent)))
            if similarity > stu_plag.ref1_similarity:
                stu_plag.ref1_similarity = similarity
                stu_plag.ref1_content = ref1_sent
        for ref2_sent in ref2_sents:
            similarity = len(lcs.PlagDetect.rmmlsslst(lcs.PlagDetect.lcs(sent, ref2_sent))) / float(len(lcs.PlagDetect.rmmlsslst(sent)))
            if similarity > stu_plag.ref2_similarity:
                stu_plag.ref2_similarity = similarity
                stu_plag.ref2_content = ref2_sent
        stu_plag_list.append(stu_plag)
    return stu_plag_list


if __name__ == '__main__':
    # prepare ref data
    prepare_ref_data()
    # Connect to moodle_db database
    cnx = mysql.connector.connect(user=MOODLE_DB_USERNAME, password=MOODLE_DE_PWD, host=MOODLE_DB_HOST, database=MOODLE_DB_DBNAME, charset='utf8mb4')
    cur = cnx.cursor(buffered=True)
    cur.execute("use " + MOODLE_DB_DBNAME)

    student_role_id = 5

    cur.execute("TRUNCATE TABLE mdl_workshop_plag")
    cur.execute("TRUNCATE TABLE mdl_workshop_plag_report")
    cur.execute(""" SELECT m_u.id, m_u.lastname, m_u.firstname, m_u.username, m_u.email, m_ws.title, m_ws.content, m_ws.grade
                    FROM mdl_workshop_submissions AS m_ws
                    INNER JOIN mdl_user AS m_u ON m_ws.authorid = m_u.id
                    INNER JOIN mdl_role_assignments AS m_rs ON m_ws.authorid = m_rs.userid
                    WHERE m_rs.roleid = '""" + str(student_role_id) + "'")
    stu_asgn_info_list = cur.fetchall()

    # prepare student assignment data from database
    stu_assgn_data_from_db(stu_asgn_info_list)

    for stu_asgn in STU_ASGN_LIST:
        plag_report_item = database_models.MdlWorkshopPlagReport()
        plag_report_item.author_id = stu_asgn.author_id
        plag_report_item.author_name = stu_asgn.last_name + stu_asgn.first_name
        plag_report_item.title = stu_asgn.title
        plag_report_item.ws_grading = stu_asgn.grade
        plag_report_item.plg_cnt = 0

        print("Analyzing student: " + str(plag_report_item.author_id))
        # remove reference (title) sentence in student assignment
        STU_SENTS = stu_sents_from_content(stu_asgn.content)
        plag_report_item.sentence_cnt = len(STU_SENTS)

        # calculate plag report
        STU_PLAG_LIST = stu_plag_report(stu_asgn.author_id, STU_SENTS, REF1_SENTS, REF2_SENTS)


        for stu_plag_item in STU_PLAG_LIST:
            if stu_plag_item.ref1_similarity > PLAG_THRESHOLD or stu_plag_item.ref2_similarity > PLAG_THRESHOLD:
                plag_report_item.plg_cnt += 1

            # insert into mdl_workshop_plag
            cur.execute(""" INSERT INTO mdl_workshop_plag (author_id, sentence_id, sentence_content,
                            ref1_content, ref1_similarity, ref2_content, ref2_similarity)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (stu_plag_item.author_id, stu_plag_item.sentence_id,
                             stu_plag_item.sentence_content,
                             stu_plag_item.ref1_content, stu_plag_item.ref1_similarity,
                             stu_plag_item.ref2_content, stu_plag_item.ref2_similarity))
            cnx.commit()
            print(" INSERT INTO mdl_workshop_plag ...")

        plag_report_item.plg_cent = float(plag_report_item.plg_cnt) / float(plag_report_item.sentence_cnt)
        # insert into mdl_workshop_plag_report
        cur.execute(""" INSERT INTO mdl_workshop_plag_report (author_id, author_name, title,
                        sentence_cnt, plg_cnt, plg_cent, ws_grading)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (plag_report_item.author_id, plag_report_item.author_name,
                     plag_report_item.title, plag_report_item.sentence_cnt,
                     plag_report_item.plg_cnt, plag_report_item.plg_cent,
                     plag_report_item.ws_grading))
        cnx.commit()
        print(" INSERT INTO mdl_workshop_plag_report ...")
        # REPORT_LIST.append(plag_report_item)
    cur.close()















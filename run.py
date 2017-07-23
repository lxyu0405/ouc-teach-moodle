# -*- coding: utf8 -*-
import uniout
import mysql.connector
import ConfigParser
import sys
import csv
import time
reload(sys)
sys.setdefaultencoding('utf-8')


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
MOODLE_DB_DBNAME = CONFIG.get('moodle_db', 'db_name')
# references infomation
REF1_TITLE = CONFIG.get('references', 'ref1_title')
REF1_DIR = CONFIG.get('references', 'ref1_dir')
REF2_TITLE = CONFIG.get('references', 'ref2_title')
REF2_DIR = CONFIG.get('references', 'ref2_dir')

sys.path.append(SLN_DIR + 'model')
sys.path.append(SLN_DIR + 'utils')

from stu_plag import StuPlag
from char_tools import CharTools
from lcs import PlagDetect
from stu_asgn_info import StuAsgnInfo
from csv_report_struct import CSVReportStruct

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f s' % (f.func_name, time2-time1)
        return ret
    return wrap


STU_ASGN_LIST = []
REF1_SENTS = []
REF2_SENTS = []
REF_TITLE = []
REPORT_LIST = []

@timing
def prepare_ref_data():
    # prepare sentences data for ref1
    for line in open(SLN_DIR + REF1_DIR):
        for sent in PlagDetect.cut_sentence(line):
            this_sent = CharTools.clean_spaces(sent)
            if len(this_sent) > 6:
                REF1_SENTS.append(this_sent)
    for sent in PlagDetect.cut_sentence(REF1_TITLE):
        REF_TITLE.append(sent)

    # prepare sentences data for ref2
    for line in open(SLN_DIR + REF2_DIR):
        for sent in PlagDetect.cut_sentence(line):
            this_sent = CharTools.clean_spaces(sent)
            if len(this_sent) > 6:
                REF2_SENTS.append(this_sent)
    for sent in PlagDetect.cut_sentence(REF2_TITLE):
        REF_TITLE.append(sent)

@timing
def stu_assgn_data_from_db(db_list):
    for item in db_list:
        stu_asgn_item = StuAsgnInfo()
        stu_asgn_item.last_name = item[0]
        stu_asgn_item.first_name = item[1]
        stu_asgn_item.username = item[2]
        stu_asgn_item.email = item[3]
        stu_asgn_item.title = item[4]
        # clean the content
        # remove html tags e.g. '<h1></h1>'
        # remove spaces, meaningless symbol, nbsp
        stu_asgn_item.content = CharTools.clean_nbsp(CharTools.clean_meaningless_symbol(
            CharTools.clean_spaces(CharTools.clean_html_tags(item[5]))))
        stu_asgn_item.grade = item[6]
        STU_ASGN_LIST.append(stu_asgn_item)

@timing
def stu_sents_from_content(str_content):
    stu_sent_list = []
    for sent in PlagDetect.cut_sentence(str_content):
        for ref_title in REF_TITLE:
            # remove reference (title) sentence in student assignment
            if ref_title not in sent and len(sent) > 6:
                stu_sent_list.append(sent)
                break
    return stu_sent_list


@timing
def stu_plag_report(stu_sents, ref1_sents, ref2_sents):
    stu_plag_list = []
    for sent in stu_sents:
        stu_plag = StuPlag()
        stu_plag.stu_sent = sent
        for ref1_sent in ref1_sents:
            similarity = len(PlagDetect.rmmlsslst(PlagDetect.lcs(sent, ref1_sent))) / float(len(sent))
            if similarity > stu_plag.similarity1:
                stu_plag.similarity1 = similarity
                stu_plag.ref1_sent = ref1_sent
        for ref2_sent in ref2_sents:
            similarity = len(PlagDetect.rmmlsslst(PlagDetect.lcs(sent, ref2_sent))) / float(len(sent))
            if similarity > stu_plag.similarity2:
                stu_plag.similarity2 = similarity
                stu_plag.ref2_sent = ref2_sent
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

    cur.execute(""" SELECT m_u.lastname, m_u.firstname, m_u.username, m_u.email, m_ws.title, m_ws.content, m_ws.grade
                    FROM mdl_workshop_submissions AS m_ws
                    INNER JOIN mdl_user AS m_u ON m_ws.authorid = m_u.id
                    INNER JOIN mdl_role_assignments AS m_rs ON m_ws.authorid = m_rs.userid
                    WHERE m_rs.roleid = '""" + str(student_role_id) + "'")
    stu_asgn_info_list = cur.fetchall()

    # prepare student assignment data from database
    stu_assgn_data_from_db(stu_asgn_info_list)

    for stu_asgn in STU_ASGN_LIST:
        csv_report_item = CSVReportStruct()
        csv_report_item.name = stu_asgn.last_name + stu_asgn.first_name
        csv_report_item.title = stu_asgn.title
        csv_report_item.peer_grade = stu_asgn.grade

        print(u"Analyzing student: " + csv_report_item.name)
        # remove reference (title) sentence in student assignment
        STU_SENTS = stu_sents_from_content(stu_asgn.content)

        # calculate plag report
        STU_PLAG_LIST = stu_plag_report(STU_SENTS, REF1_SENTS, REF2_SENTS)

        with open(SLN_DIR + 'reports/' + csv_report_item.name + '--分析报告.csv', 'wb') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(['学生句子', '参考文献1中句子', '相似度1', '参考文献2中句子', '相似度2'])
            for stu_plag_item in STU_PLAG_LIST:
                writer.writerow([(stu_plag_item.stu_sent).encode('utf-8'), (stu_plag_item.ref1_sent).encode('utf-8'), stu_plag_item.similarity1, (stu_plag_item.ref2_sent).encode('utf-8'), stu_plag_item.similarity2])
        f.close()
        









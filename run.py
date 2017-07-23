# -*- coding: utf8 -*-
import uniout
import mysql.connector
import ConfigParser
import sys
import csv


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

STU_ASGN_LIST = []
REF1_SENTS = []
REF2_SENTS = []

if __name__ == '__main__':
    # prepare sentences data for ref1
    for line in open(SLN_DIR + REF1_DIR):
        for sent in PlagDetect.cut_sentence(line):
            this_sent = CharTools.clean_spaces(sent)
            if len(this_sent) > 8:
                REF1_SENTS.append(this_sent)
    # prepare sentences data for ref2
    for line in open(SLN_DIR + REF2_DIR):
        for sent in PlagDetect.cut_sentence(line):
            this_sent = CharTools.clean_spaces(sent)
            if len(this_sent) > 8:
                REF2_SENTS.append(this_sent)

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

    for item in stu_asgn_info_list:
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



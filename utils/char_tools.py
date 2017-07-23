# -*- coding: utf8 -*-
import re


class CharTools(object):
    @staticmethod
    def clean_html_tags(raw_html_content):
        cleaner = re.compile('<.*?>')
        return re.sub(cleaner, '', raw_html_content)

    @staticmethod
    def clean_nbsp(raw_content):
        cleaner = re.compile('&nbsp;')
        return re.sub(cleaner, '', raw_content)

    @staticmethod
    def clean_spaces(raw_content):
        # clear meaningless space
        cleaner = re.compile('\s+')
        return re.sub(cleaner, '', raw_content)

    @staticmethod
    def clean_alph(content):
        cleaner = re.compile('[a-zA-Z]')
        return re.sub(cleaner, '', content)

    @staticmethod
    def clean_meaningless_symbol(raw_content):
        # clear meaningless dot in Content
        cleaner_dot = re.compile('\.{7,}')
        cleaner_dot_text = re.sub(cleaner_dot, ' ', raw_content)
        # clear meaningless - in Content
        content = cleaner_dot_text.replace('-', '').replace('_', '').replace(u'●', u'。')
        return content

    @staticmethod
    def rmmlsslst(lst): #remove meaningless word in list
        lcs_list = []
        stop_words = [u'的', u'了']
        for word in lst:
            if word in ',.!?;~，。！？；～'.decode('utf8'):
                continue
            if word in stop_words:
                continue
            lcs_list.append(word)
        return lcs_list
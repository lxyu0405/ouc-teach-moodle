# -*- coding: utf8 -*-
import re


class CharTools(object):
    # 去除html标签
    @staticmethod
    def clean_html_tags(raw_html_content):
        cleaner = re.compile('<.*?>')
        return re.sub(cleaner, '', raw_html_content)

    # 去除 &nbsp标志
    @staticmethod
    def clean_nbsp(raw_content):
        cleaner = re.compile('&nbsp;')
        return re.sub(cleaner, '', raw_content)

    # 去除spaces
    @staticmethod
    def clean_spaces(raw_content):
        # clear meaningless space
        cleaner = re.compile('\s+')
        return re.sub(cleaner, '', raw_content)

    # 去除英文单词
    @staticmethod
    def clean_alph(content):
        cleaner = re.compile('[a-zA-Z]')
        return re.sub(cleaner, '', content)

    # 去除无意义符号
    @staticmethod
    def clean_meaningless_symbol(raw_content):
        # clear meaningless dot in Content
        cleaner_dot = re.compile('\.{7,}')
        cleaner_dot_text = re.sub(cleaner_dot, ' ', raw_content)
        # clear meaningless - in Content
        content = cleaner_dot_text.replace('-', '').replace('_', '').replace(u'●', u'。')
        return content

    # 去除中文句子中无意义的介词、语气词
    # 该词典有目的的填充可影响分析结果
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
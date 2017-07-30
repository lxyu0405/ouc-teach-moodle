# -*- coding: utf8 -*-
import re
import csv


class PlagDetect(object):

    # 通过标点切割文本
    @staticmethod
    def cut_sentence(words):
        words = (words).decode('utf8') #如果是从编码为 utf8 的 txt 文本中直接输入的话，需要先把文本解码成 unicode 来处理
        start = 0
        i = 0  #记录每个字符的位置
        sents = []
        punt_list = ',.!?:;~，。！？：；～'.decode('utf8')  #string 必须要解码为 unicode 才能进行匹配
        for word in words:
            if word in punt_list:
                sents.append(words[start:i+1])
                start = i + 1  #start标记到下一句的开头
                i += 1
            else:
                i += 1  #若不是标点符号，则字符位置继续前移
        if start < len(words):
            sents.append(words[start:])  #这是为了处理文本末尾没有标点符号的情况
        return sents

    # 计算两个句子的最长子序列内容和长度
    # 使用动态规划方法优化
    @staticmethod
    def lcs(x, y):
        n = len(x)
        m = len(y)
        table = dict()  # a hashtable, but we'll use it as a 2D array here

        for i in range(n+1):     # i=0,1,...,n
            for j in range(m+1):  # j=0,1,...,m
                if i == 0 or j == 0:
                    table[i, j] = 0
                elif x[i-1] == y[j-1]:
                    table[i, j] = table[i-1, j-1] + 1
                else:
                    table[i, j] = max(table[i-1, j], table[i, j-1])

        # Now, table[n, m] is the length of LCS of x and y.

        # Let's go one step further and reconstruct
        # the actual sequence from DP table:

        def recon(i, j):
            if i == 0 or j == 0:
                return []
            elif x[i-1] == y[j-1]:
                return recon(i-1, j-1) + [x[i-1]]
            elif table[i-1, j] > table[i, j-1]: #index out of bounds bug here: what if the first elements in the sequences aren't equal
                return recon(i-1, j)
            else:
                return recon(i, j-1)

        return recon(n, m)

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

    # 去除中文句子中无意义的介词、语气词
    # 该词典有目的的填充可影响分析结果
    @staticmethod
    def rmmlssstr(str): #remove meaningless word in str
        res_str = ""
        stop_words = [u'的', u'了']
        for word in str:
            if word in ',.!?;~，。！？；～'.decode('utf8'):
                continue
            if word in stop_words:
                continue
            res_str += word
        return res_str

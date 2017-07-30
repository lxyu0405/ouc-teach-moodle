# -*- coding: utf8 -*-


class StuAsgnInfo:
    # 学生用户id，与mdl_user表关联
    author_id = 0
    # 学生姓
    last_name = u''
    # 学生名
    first_name = u''
    # 学生帐号登陆名
    username = ''
    # 学生email
    email = ''
    # 学生文章标题
    title = u''
    # 学生文章内容
    # 使用CharTools类中方法做'去html标签'、'去spaces'、'去无意义字符'处理后的纯文本数据
    content = u''
    # 学生互评阶段成绩
    grade = 0.0

    def __init__(self):
        self.author_id = 0
        self.last_name = u''
        self.first_name = u''
        self.username = ''
        self.email = ''
        self.title = u''
        self.content = u''
        self.grade = 0.0
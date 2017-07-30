## 1 项目部署&运行
### 1.1 项目部署
* 登陆服务器
	- Linux & MacOS: `ssh ubuntu@118.89.103.53`
	- Windows请使用putty
* 项目采用Git的形式部署，每次进入服务器 `/home/ubuntu/ouc-teach-platform/ouc-teach-moodle` 目录后，执行`git pull`以获取最新代码。
	
### 1.2 运行方法
*	进入对应项目目录
	`cd /home/ubuntu/ouc-teach-platform/ouc-teach-moodle`
*	修改相关配置（若有需要）
	`vi config.conf`
*	运行 run.py（用专为本项目配置的python虚拟环境）
	`/home/ubuntu/ouc-teach-platform/ouc-virtualenv/bin/python run.py`
		



## 2 项目结构介绍
###	2.1 run.py
* 主函数入口，包含分析的主要逻辑。
	
### 2.2 config.conf 配置文件

|配置名|说明|
|:----    |:---|
|project.dir |项目路径  |
|project.name |项目名  |
|project.author     |项目作者  |
|moodle_db.username |数据库用户名  |
|moodle_db.password |数据库密码  |
|moodle_db.db_host     |数据库host（一般localhost即可）  |
|moodle_db.port |数据库端口号（一般3306）  |
|moodle_db.db_name |数据库名（moodle_db）  |
|references.ref1_title     |参考文献1标题  |
|references.ref1_dir |参考文献1所在路径  |
|references.ref2_title |参考文献2标题  |
|references.ref2-dir     |参考文献2所在路径  |
	
### 2.3 model
#### 2.3.1 database_models.py
	主要存储与数据库表结构对应的类。Class `MdlWorkshopPlag`和`MdlWorkshopPlagReport`分别对应Table`mdl_workshop_plag`和`mdl_workshop_plag_report`。（由于现在涉及到表和表操作数量不多，使用Python ORM框架得不偿失。等涉及到数量多了以后，可以采用 SQLAlchemy和SQLACodegen进一步框架化项目）
	
- MdlWorkshopPlagReport

|属性名|类型|说明|
|:----    |:----- |-----   |
|author_id |int |学生用户id   |
|author_name |string | 学生姓名    |
|title     |string | 学生文章标题    |
|sentence_cnt |int |学生文章中有效句子数量   |
|plg_cnt |int | 学生文章中可疑抄袭句子数量    |
|plg_cent     |float | 学生文章中可疑抄袭句子比例    |
|ws_grading |float |该学生在互评阶段的成绩   |
- MdlWorkshopPlag

|属性名|类型|说明|
|:----    |:----- |-----   |
|plag_id |int |PK, AI   |
|author_id |int | 学生用户id    |
|sentence_id     |int | 学生句子id    |
|sentence_content |string |学生句子内容   |
|ref1_content |string | 与参考文献1中最相似的句子    |
|ref1_similarity     |float | 与参考文献1中最相似句子的相似度    |
|ref2_content |string |与参考文献2中最相似的句子   |
|ref2_similarity     |float | 与参考文献2中最相似句子的相似度    |
#### 2.3.2 stu_asgn_info.py
	主要存储分析逻辑中设计到的数据结构。
- StuAsgnInfo

|属性名|类型|说明|
|:----    |:----- |-----   |
|author_id |int |学生用户id，与mdl_user表关联   |
|last_name |string | 学生姓    |
|first_name     |string | 学生名    |
|username |string |学生帐号登陆名   |
|email |string | 学生email    |
|title     |string | 学生文章标题    |
|content |string |学生文章内容   |
|grade |float |学生互评阶段成绩   |

###	2.4 resources
* 放置资源文件，参考文献的文本内容放置位置
* moodle_db_2017*.sql 
	moodle_db数据库备份
* plag_tables.sql
	创建项目DIY的两张表













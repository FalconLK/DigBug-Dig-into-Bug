#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''수정 경로 145'''
############Stackoverflow Indexing Code############

import sys
sys.path.append(".")
sys.path.append("..")
sys.path.append("...")

sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/jsoup-1.8.2.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/lucene-analyzers-common-4.10.4.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/lucene-core-4.10.4.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/lucene-queries-4.10.4.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/lucene-queryparser-4.10.4.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/jython-standalone-2.7.0.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/mysql-connector-java-5.1.22-bin.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/py4j-0.9.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.apache.commons.lang_2.6.0.v201205030909.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.cdt.core_5.6.0.201402142303.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.core.contenttype_3.4.200.v20120523-2004.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.core.jobs_3.5.200.v20120521-2346.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.core.resources.win32.x86_3.5.100.v20110423-0524.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.core.resources_3.8.0.v20120522-2034.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.core.runtime_3.8.0.v20120521-2346.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.equinox.common_3.6.100.v20120522-1841.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.equinox.common_3.6.200.v20130402-1505.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.equinox.preferences_3.5.0.v20120522-1841.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.jdt.core_3.8.1.v20120531-0637.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.jdt.ui_3.8.2.v20130107-165834.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.jface.text_3.8.0.v20120531-0600.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.ltk.core.refactoring_3.6.100.v20130605-1748.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.osgi_3.8.0.v20120529-1548.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/org.eclipse.text_3.5.0.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/bson-3.0.2.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/mongodb-driver-3.0.2.jar")
sys.path.append("/home/ubuntu/Desktop/FaCoY/GitSearch/Libs/mongodb-driver-core-3.0.2.jar")

# Description: Goes trough mysql database. extracts code snippets and buid an AST of that code. Then, the AST code information are stored in lucene/mongo

from java.sql import ResultSet
from java.sql import Connection
from java.io import File
from java.io import IOException
from java.lang import Integer
from java.lang import String

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.document import Document, Field, StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, CorruptIndexException
from org.apache.lucene.store import SimpleFSDirectory, LockObtainFailedException
from org.apache.lucene.util import Version
from java.util.concurrent import Executors

from GitSearch.MyUtils import unescape_html, tokenize
from Analyzer.PorterAnalyzer import PorterAnalyzer
from Analyzer.JavaCodeAnalyzer import JavaCodeAnalyzer
from Indexer.SOParser import PostParser
from Import.ImportAST import transform_body
from Indexer._Counter import Counter
from java.sql import SQLException
import time, codecs, shutil, os

#Jython cannot read large files (1.6MB)

pool = Executors.newFixedThreadPool(4)

path_notIndexed = "/home/ubuntu/Desktop/FaCoY/temp/not_indexed_a.txt"

def cleanMetaPath(path):
	for the_file in os.listdir(path):
		file_path = os.path.join(path, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print(e)

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if os.path.isdir(path):
			pass
		else:
			raise

def load_so_fail_ids():
	""" Contains tmp list of stackoverflow discussions which are not indexed by the JavaCodeSnippetIndexer because of failures or non-java snippets """
	with open(path_notIndexed, "r") as f:
		for line in f:
			yield int(line)

def write_file_a(file_path, content):
	with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
		file.write(content + "\n")

def get_db_connection():
	from java.lang import Class
	from java.sql import DriverManager
	Class.forName("com.mysql.jdbc.Driver")
	newConn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/stackoverflow?autoReconnect=true", "root", "djaak123")
	newConn.setAutoCommit(True)
	return newConn

def getAllIds(mysql_conn, ids_file):
	ids = list()
	stmt = mysql_conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)
	querySO = """SELECT id from posts limit 0, 10000000"""
	stmt.setFetchSize(Integer.MIN_VALUE)
	resultSet = stmt.executeQuery(querySO)

	while resultSet.next():
		ids.append(resultSet.getString("Id"))

	for id in ids:
		write_file_a(ids_file, id)
	return ids

def getQuestionDescriptions(id, mysql_conn, description_path):
	description = ''
	stmt = mysql_conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)

	# querySO = """SELECT Id, AcceptedAnswerId, Body, IF(AcceptedAnswerId, AcceptedAnswerId, Body) as description FROM posts where id = %s;""" % id
	# querySO = """select body as description from posts where id = %s """ % id
	# querySO = """select Body as description from posts where id = %s and AcceptedAnswerId is null""" %id
	# querySO = """select answer_posts.body from posts origin_posts left join posts answer_posts on origin_posts.acceptedanswerid = answer_posts.id where origin_posts.id = %s""" % id

	querySO = """SELECT (CASE WHEN ORIGIN_POST.BODY IS NOT NULL THEN ORIGIN_POST.BODY ELSE ANSWER_POST.BODY END) as description 
		FROM posts ORIGIN_POST LEFT JOIN posts ANSWER_POST ON ANSWER_POST.PARENTID = ORIGIN_POST.ID 
		WHERE ORIGIN_POST.ID = %s""" % (id)

	stmt.setFetchSize(Integer.MIN_VALUE)
	resultSet = stmt.executeQuery(querySO)

	while resultSet.next():
		description = resultSet.getString("description")
	if description:
		write_file_a(description_path + str(id) + '.txt', description)
	return description
	pass

def getQuestionTags(id, mysql_conn, description_path):
	pass

def getQuestionDescriptionsAndTags(id, mysql_conn):
	description = ''
	tags = ''
	stmt = mysql_conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)

	# querySO = """SELECT Id, AcceptedAnswerId, Body, IF(AcceptedAnswerId, AcceptedAnswerId, Body) as description FROM posts where id = %s;""" % id
	# querySO = """select body as description from posts where id = %s """ % id
	# querySO = """select Body as description from posts where id = %s and AcceptedAnswerId is null""" %id
	# querySO = """select answer_posts.body from posts origin_posts left join posts answer_posts on origin_posts.acceptedanswerid = answer_posts.id where origin_posts.id = %s""" % id

	# querySO = """SELECT BODY description FROM posts WHERE ID = %s""" % (id)
	querySO = """SELECT (CASE WHEN ORIGIN_POST.BODY IS NOT NULL THEN ORIGIN_POST.BODY ELSE ANSWER_POST.BODY END) as description, ORIGIN_POST.TAGS as tags
		FROM posts ANSWER_POST LEFT JOIN posts ORIGIN_POST ON ANSWER_POST.PARENTID = ORIGIN_POST.ID 
		WHERE ANSWER_POST.ID = %s""" % (id)

	stmt.setFetchSize(Integer.MIN_VALUE)
	resultSet = stmt.executeQuery(querySO)

	while resultSet.next():
		description = resultSet.getString("description")
		tags = resultSet.getString("tags")

	# print 'Description: ', description
	# print '\nTAG: ', tags
	# write_file_a(description_path + '/question' + str(id) + '.txt', description)
	# write_file_a(description_path + '/tags' + str(id) + '.txt', str(tags))
	return description, tags

def getAnswerDescriptions(id, mysql_conn):
	description = ''
	stmt = mysql_conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)

	# querySO = """SELECT Id, AcceptedAnswerId, Body, IF(AcceptedAnswerId, AcceptedAnswerId, Body) as description FROM posts where id = %s;""" % id
	# querySO = """select body as description from posts where id = %s """ % id
	# querySO = """select Body as description from posts where id = %s and AcceptedAnswerId is null""" %id
	# querySO = """select answer_posts.body from posts origin_posts left join posts answer_posts on origin_posts.acceptedanswerid = answer_posts.id where origin_posts.id = %s""" % id

	querySO = """SELECT (CASE WHEN ANSWER_POST.BODY IS NOT NULL THEN ANSWER_POST.BODY ELSE ORIGIN_POST.BODY END) as description 
	FROM posts ORIGIN_POST LEFT JOIN posts ANSWER_POST ON ORIGIN_POST.ACCEPTEDANSWERID = ANSWER_POST.ID 
	WHERE ORIGIN_POST.ID = %s""" % (id)

	stmt.setFetchSize(Integer.MIN_VALUE)
	resultSet = stmt.executeQuery(querySO)

	while resultSet.next():
		description = resultSet.getString("description")

	# print "Description: ", description
	# write_file_a(description_path + str(id) + '.txt', description)
	return description

if __name__ == '__main__':
	print ('start..')
	base_path = '/extdsk'
	ids_file = base_path + '/stack_ids.txt'
	description_path = base_path + '/stack_descriptions_by_ids/'

	##### Clean the dst paths
	# if os.path.isfile(ids_file):
	# 	os.remove(ids_file)

	# if not os.path.isdir(description_path):
	# 	mkdir_p(description_path)
	# else:
	# 	cleanMetaPath(description_path)

	##### ID file generating
	# id_list = getAllIds(mysql_conn, ids_file)

	##### ID file reading
	from GitSearch.MyUtils import read_file
	contents = read_file(ids_file)
	id_list = list()
	for i in contents.split('\n'):
		id_list.append(i)

	##### Contents savings	 현재 다 저장하기에는 무리가 있고, 골라저 저장해야한다.
	mysql_conn = get_db_connection()
	number_of_ids = len(id_list)
	for idx, id in enumerate(id_list):
		print '---------------------------------------------------------------------------------------'
		print('ID: %s /// Processing %s/%s...' % (id, idx + 1, number_of_ids))

		q_description = getQuestionDescriptionsAndTags(id, mysql_conn, description_path)
		print ''
		a_description = getAnswerDescriptions(id, mysql_conn, description_path + 'answer/')

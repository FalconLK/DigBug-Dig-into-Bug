# Author: Sirres Raphael
# Description: Goes trough mysql database. extracts code snippets and buid an AST of that code. Then, the AST code information are stored in lucene/mongo

from java.sql import Connection
from java.sql import ResultSet
from java.sql import SQLException
from java.sql import Statement

from java.io import File
from java.io import IOException

from java.lang import Integer
from java.lang import String

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.document import Document, Field, NumericDocValuesField,StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, CorruptIndexException
from org.apache.lucene.store import SimpleFSDirectory, LockObtainFailedException
from org.apache.lucene.store import RAMDirectory
from org.apache.lucene.util import Version
from java.util.concurrent import Executors, TimeUnit

import utils
from PorterAnalyzer import PorterAnalyzer
from JavaCodeAnalyzer import JavaCodeAnalyzer

from SOParser import PostParser

from ImportAST import transform_body
#from NewJavaParser import parse

# Jython cannot read large files (1.6MB)


pool = Executors.newFixedThreadPool(4)

def load_so_fail_ids(path="/Users/Raphael/Dropbox/uni.lu/Master/SEM.4/GitSearch/Resources/not_indexed.txt"):
	""" Contains tmp list of stackoverflow discussions which are not indexed by the JavaCodeSnippetIndexer because of failures or non-java snippets """
	with open(path, "r") as f:
		for line in f:
			yield int(line)

def index_code_snippet(writer):
	mysql_conn = utils.get_db_connection()

	stmt = mysql_conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)

	querySO = 	"""	SELECT Q.Id as QId, Q.Title, Q.Body as QBody, Q.Tags, Q.ViewCount, Q.Score, A.Body as ABody, A.Id as AId FROM posts as Q 
					JOIN posts as A ON Q.Id = A.ParentId
					WHERE A.AcceptedAnswer = 1 AND A.Score > 0 AND A.Body LIKE "%</code>%" 
					AND	LOWER(Q.Title) NOT LIKE "%not%" 
					AND LOWER(Q.Title) NOT LIKE "%why%" 
					AND LOWER(Q.Title) NOT LIKE "%error%" 
					AND LOWER(Q.Title) NOT LIKE "%no %" 
					AND LOWER(Q.Title) NOT LIKE "% install%"
					AND LOWER(Q.Title) NOT LIKE "% can't%"
					AND LOWER(Q.Title) NOT LIKE "% don't%"
					AND LOWER(Q.Title) NOT LIKE "% issue%"
					AND LOWER(Q.Title) NOT LIKE "difference %"
					AND LOWER(Q.Title) NOT LIKE "unable %"
					AND LOWER(Q.Title) NOT LIKE "debug %"
					AND LOWER(Q.Title) NOT LIKE "exception %"
					AND LOWER(Q.Title) NOT LIKE "best way %"
				""" # Returns nearly 400.000 posts 
					#AND Q.CreationDate < "2014-01-01 00:00:00"

					#AND A.CreationDate < "2013-06-01 00:00:00" 

	stmt.setFetchSize(Integer.MIN_VALUE)
	rs = stmt.executeQuery(querySO)
	i = 0
	not_indexed = []

	failed_id_gen = load_so_fail_ids()
	failed_id = next(failed_id_gen, None)
	while rs.next():
		i += 1
		if i % 1000 == 0:
			print "C: %s" % (i)
			
		#print "hallo"
		question_id = rs.getInt("QId")
		answer_id = rs.getInt("AId")
		title = rs.getString("Title")
		#question_body = SOParser.clean_question(utils.unescape_html(rs.getString("QBody")))
		# tags = rs.getString("Tags").replace("><", " ").replace("<","").replace(">","")
		view_count = rs.getString("ViewCount")
		score = rs.getInt("Score")
		qbody = utils.so_text(rs.getString("QBody"))
		abody = rs.getString("ABody")
		#abodytext = utils.so_text((rs.getString("ABody")))

		#print question_id, failed_id
		if question_id == failed_id:
			# Get next failed id
			failed_id = next(failed_id_gen, None)
			#print "Omit question: %s" % failed_id
			continue

		document = Document()
		document.add(StringField("id", String.valueOf(question_id), Field.Store.YES))
		document.add(StringField("answer_id", String.valueOf(answer_id), Field.Store.YES))
		document.add(Field("title", title, Field.Store.YES, Field.Index.ANALYZED))

		p = PostParser(abody)
		document.add(StringField("description", p.first_description(), Field.Store.YES))
		# document.add(Field("qbody", qbody, Field.Store.YES, Field.Index.ANALYZED))
		# document.add(Field("abody", abodytext, Field.Store.YES, Field.Index.ANALYZED ))

		# for tag in tags.split():
		# 	if tag:
		# 		document.add(Field("tags", tag, Field.Store.YES, Field.Index.ANALYZED ))

		document.add( Field("view_count", view_count, Field.Store.YES, Field.Index.ANALYZED))

		if add_code_into_document(document, abody):
		#add_code_from_mongo(document, coll, answer_id)
			writer.addDocument(document)
		else:
			#print "Not Indexed: %s" % question_id
			not_indexed.append(question_id)
		#parse java code

	print "Not Index: %s" % len(not_indexed)
	#utils.write_file("/tmp/not_indexed.txt", str(not_indexed))
		
def add_code_into_document(document, body):
	asts, code_hints = transform_body(body)

	flag = False

	#typed_method_call = set()
	for ast in asts:
		for mc in ast["typed_method_call"]:
			if mc:
				document.add( Field("typed_method_call", mc, Field.Store.YES, Field.Index.ANALYZED))
				flag = True

		for e in ast["extends"]:
			if e:
				document.add(Field("extends", e, Field.Store.YES,Field.Index.ANALYZED))

		for c in ast["used_classes"]:
			if c:
				document.add( Field("used_classes", c, Field.Store.YES, Field.Index.ANALYZED))

		for m in ast["methods"]:
			if m:
				document.add(Field("methods", m, Field.Store.YES, Field.Index.ANALYZED))
				flag = True

		for m in ast["methods_called"]:
			if m:
				document.add(Field("methods_called", m, Field.Store.YES, Field.Index.ANALYZED))
				flag = True

		#comment
		if "comments" in ast:
			for c in ast["comments"]:
				document.add(Field("comments", utils.unescape_html(c), Field.Store.NO, Field.Index.ANALYZED))

		for i in ast["class_instance_creation"]:
			if i:
				document.add(Field("class_instance_creation", i, Field.Store.YES , Field.Index.ANALYZED))
				flag = True

		for l in ast["literals"]:
			if l:
				document.add( StringField("literals", l, Field.Store.YES))
		
		#finally all the splitted words
		# for s in camel_case:
		# 	document.add( Field("camel_case_words", s.lower(), Field.Store.NO, Field.Index.NOT_ANALYZED))

	hints = []
	for h in code_hints:
		for token in utils.tokenize(h):
			if 1 < len(token) < 20:
				hints.append(token)

	for hint in set(hints):
		document.add(Field("code_hints", hint, Field.Store.YES, Field.Index.ANALYZED))

	return flag


def main():
	INDEX_DIR = "indexes"
	try:
		print "Indexing..."
		indexDir = File("/Users/Raphael/Downloads/stackoverflow1107")

		#writer = IndexWriter(SimpleFSDirectory(indexDir), StandardAnalyzer(), True, IndexWriter.MaxFieldLength.UNLIMITED)
		analyzer = PorterAnalyzer( StandardAnalyzer(Version.LUCENE_CURRENT))
		a = {	"typed_method_call": KeywordAnalyzer(), "extends": KeywordAnalyzer(), 
				"used_classes": KeywordAnalyzer(), "methods": KeywordAnalyzer(), 
				"class_instance_creation": KeywordAnalyzer(), "methods_called": KeywordAnalyzer(), "view_count" : KeywordAnalyzer(), "code_hints": JavaCodeAnalyzer() }
		wrapper_analyzer = PerFieldAnalyzerWrapper(analyzer, a)
		config = IndexWriterConfig(Version.LUCENE_CURRENT, wrapper_analyzer)
		writer = IndexWriter(SimpleFSDirectory(indexDir), config)

		index_code_snippet(writer)

		writer.commit()
		writer.close()
		print "Done"
	except CorruptIndexException as e:		#when index is corrupt
			e.printStackTrace()
	except LockObtainFailedException as e:	#when other writer is using the index
			e.printStackTrace()
	except IOException as e:	#when directory can't be read/written
			e.printStackTrace()
	except SQLException as e: 	#when Database error occurs
			e.printStackTrace()

if __name__ == '__main__':
	main()

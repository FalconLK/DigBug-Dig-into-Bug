#!/usr/bin/env python
# -*- coding: utf-8 -*-

from java.io import File
from java.io import IOException

from java.lang import Integer
from java.lang import String

from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.document import Document, Field, NumericDocValuesField, StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, CorruptIndexException
from org.apache.lucene.store import SimpleFSDirectory, LockObtainFailedException
from org.apache.lucene.util import Version


from zlib import compress, decompress
from utils import unescape_html, camel_case_split, md5, so_tokenizer

from ImportAST import parallize

# Paralell Execution of Parser
from java.util.concurrent import Executors, TimeUnit


import os
import codecs
import traceback


from PorterAnalyzer import PorterAnalyzer
from JavaCodeAnalyzer import JavaCodeAnalyzer

#from JavaCodeParser import parse, JDTParser
from NewJavaParser import parse



def java_files_from_dir(directory):
	javafiles = (os.path.join(dirpath, f)
	    for dirpath, dirnames, files in os.walk(directory)
	    for f in files if f.endswith('.java'))
	return javafiles


# def queue_concurrency(queue, doc_source, num_of_tasks):
# 	queue.append(JDTParser(doc_source[1], parse))
# 	if len(queue) >= num_of_tasks:
# 		futures = pool.invokeAll(queue)
# 		asts = [ future.get(3, TimeUnit.SECONDS).result for future in futures]

# 	queue = []

# 	return doc_source[0], asts
	



hashes = set()
def index_code_snippet(writer):
	HOME = "/Users/Raphael/Downloads/GitArchive" #29.06.2015, 03.07.2015, 15.07.2015
	jfiles = java_files_from_dir(HOME)

	N_cores = 4

	# print("Number of Java files to process: %s" % (len(jfiles)))
	source_queue = []

	i = 0
	j = 0

	for jfile in jfiles:
		i += 1
		if i % 1000 == 0:
			print("Counter: %s" % i)
			break
			
		
			
		document = Document()
		document.add(Field("file", jfile, Field.Store.YES, Field.Index.NO))
		


		try:
			with codecs.open(jfile, "r", encoding='utf-8') as f:
				file_content = f.read().encode("utf-8")



			document.add( Field("file_content", compress(file_content), Field.Store.YES, Field.Index.NO) )
			# Check for duplicates files and accumulate source code
			# hash_v =  str(md5(file_content))
			# if hash_v not in hashes:
			# 	source_queue.append((document, file_content))
			# 	hashes.add(hash_v)

			# Wait until source files
			# if len(source_queue) >= N_cores:
			# 	ast_docs = parallize(source_queue)
			# 	source_queue = []

			# 	for ast, file_content, doc in ast_docs:
			ast = parse(file_content, resolve=False)
			if add_code_keyword_into_document(document, file_content, ast):
				writer.addDocument(document)
				j += 1
				if j % 1000 == 0:
					print "Wrote:: %s files" % j

		except Exception as e:
			#traceback.print_exc()
			#print jfile
			print("Error: %s" % e)
			continue

	print "Number of files: %s" % i

	print "Number of duplicates: %s" % len(hashes)

	print("%s files has been indexed" % j)
		# multi_parser = JDTParser(file_content, parse)
		# node = pool.submit(multi_parser)
		# nodes = queue_concurrency(queue, (document, file_content), 4)
		# for node in nodes:		



def add_code_keyword_into_document(document, file_content, node):

	# Flag is set when at least 1 code characteristics has been stored
	flag = False
	

	
	#document.add( Field("var_type_map", str(dict(node["var_type_map"])), Field.Store.YES, Field.Index.NO))
	document.add( Field("line_numbers", str(dict(node["line_numbers"])), Field.Store.YES, Field.Index.NO))
	document.add( Field("hash", str(md5(file_content)), Field.Store.YES, Field.Index.NO))



	# Code as Text Do we still need comments ?
	document.add( Field("code", so_tokenizer(file_content, False), Field.Store.YES, Field.Index.ANALYZED))

	for m in node["typed_method_call"]:
		if m:
			flag = True
			document.add( Field("typed_method_call", m, Field.Store.YES, Field.Index.ANALYZED))

	for e in node["extends"]:
		if e:
			document.add(Field("extends", e, Field.Store.NO, Field.Index.ANALYZED))

	for c in node["used_classes"]:
		if c:
			document.add( Field("used_classes", str(c), Field.Store.YES, Field.Index.ANALYZED))

	for i in node["class_instance_creation"]:
		if i:
			flag = True
			document.add( Field("class_instance_creation", i, Field.Store.YES, Field.Index.ANALYZED) )

	for m in node["methods"]:
		if m:
			document.add(Field("methods", m, Field.Store.YES, Field.Index.ANALYZED))

	for m in node["methods_called"]:
		if m:
			document.add(Field("methods_called", m, Field.Store.YES, Field.Index.ANALYZED))
			flag = True

	for m in node["unresolved_method_calls"]:
		if m:
			document.add(Field("unresolved_method_calls", m, Field.Store.YES, Field.Index.ANALYZED))

	for l in node["literals"]:
		if l:
			document.add( StringField("literals", l, Field.Store.YES))

	# for im in node["imports"]:
	# 	if im:
	# 		document.add( StringField("imports", im, Field.Store.YES))

	# for c in node["comments"]:
	# 	if c:
	# 		c = c.replace("//", "").replace("/*", "").replace("*/", "").lower()
	# 		document.add( Field("comments", unescape_html(c), Field.Store.NO, Field.Index.ANALYZED))

	# for cc in camel_case:
	# 	if cc:
	# 		document.add( Field("camel_case_split", cc, Field.Store.YES, Field.Index.NOT_ANALYZED))

	return flag



def main():
	INDEX_DIR = "indexes"
	try:
		print "Indexing..."
		indexDir = File("/Users/Raphael/Downloads/github2")

		#writer = IndexWriter(SimpleFSDirectory(indexDir), StandardAnalyzer(), True, IndexWriter.MaxFieldLength.UNLIMITED)
		analyzer = KeywordAnalyzer()#PorterAnalyzer( StandardAnalyzer(Version.LUCENE_CURRENT))
		a = { "code": JavaCodeAnalyzer(), "comments": EnglishAnalyzer(Version.LUCENE_CURRENT) }
		wrapper_analyzer = PerFieldAnalyzerWrapper(analyzer, a)
		config = IndexWriterConfig(Version.LUCENE_CURRENT, wrapper_analyzer)
		writer = IndexWriter(SimpleFSDirectory(indexDir), config)

		index_code_snippet(writer)

		
		writer.close()
	except CorruptIndexException as e:		#when index is corrupt
			e.printStackTrace()
	except LockObtainFailedException as e:	#when other writer is using the index
			e.printStackTrace()
	except IOException as e:	#when directory can't be read/written
			e.printStackTrace()

if __name__ == '__main__':
	main()

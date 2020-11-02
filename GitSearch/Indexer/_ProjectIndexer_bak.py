#!/usr/bin/env python
# -*- coding: utf-8 -*-
############GitHub Indexing Code############

'''수정 사항, line: 156 '''

import sys, os, time, codecs
sys.path.append(".")
sys.path.append("..")
sys.path.append("...")
sys.path.append("/home/ubuntu/Desktop/sqlite-jdbc-3.23.1.jar")
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

from java.io import File
from java.io import IOException
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.document import Document, Field, StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, CorruptIndexException
from org.apache.lucene.store import SimpleFSDirectory, LockObtainFailedException
from org.apache.lucene.util import Version

from Indexer.NewJavaParser import parse
from Analyzer.JavaCodeAnalyzer import JavaCodeAnalyzer
from Indexer._Counter import Counter
from GitSearch.MyUtils import md5, so_tokenizer, copytree, mkdir_p, cleanMetaPath
from Preprocessor import preProcessing, specialCharRemove


hashes = set()

def filtering_test_code_only(src, dst):
    progress = 0
    test_code_count = 0
    if not os.path.isdir(dst):
        os.mkdir(dst)

    project_only_test = set()
    for javafile in java_files_from_dir(src):
        progress += 1
        if progress % 1000 == 0: print 'Parsing: ', progress
        if ('test' or 'tests') in javafile.split('/'): # and 'test' in javafile.split('/')[-1]:
            test_code_count += 1
            project_path = '/'.join(javafile.split('/')[:6])#######################################Modify!!!!!!!!!!
            project_only_test.add(project_path)

    progress = 0
    for i in project_only_test:
        progress = progress + 1
        if progress % 1000 == 0: print 'Copy: ', progress
        target_destination_detail = dst + i.split('/')[5]	#######################################Modify!!!!!!!!!!!
        if not os.path.isdir(target_destination_detail):
            os.mkdir(target_destination_detail)
            copytree(i, target_destination_detail)
        else:
            print 'The directory is already existing..'

    for javafile in java_files_from_dir(dst):
        if not ('test' or 'Test') in javafile.split('/'):
            os.remove(javafile)

def filtering_only_with_test_code(src, dst):
    progress = 0
    if not os.path.isdir(dst):
        os.mkdir(dst)

    project_with_test = set()
    for dirpath, dirnames, files in os.walk(src):
        progress = progress + 1 #1429000
        if progress % 1000 == 0: print 'Parsing: ', progress
        if ('test' or 'tests') in dirpath.split('/'):
            project_with_test.add('/'.join(dirpath.split('/')[:7]))

    progress = 0
    for i in project_with_test:
        print 'Count: ', progress, 'Project: ', i
        progress = progress + 1
        if progress % 1000 == 0: print 'Copy: ', progress
        target_destination_detail = dst + '/' + i.split('/')[5]
        if not os.path.isdir(target_destination_detail):
            os.mkdir(target_destination_detail)
            copytree(i, target_destination_detail)
        else:
            print 'The directory is already existing..'

def java_files_from_dir(directory):
    javafiles = (os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(directory)
        for f in files if f.endswith('.java'))
    return javafiles



def generate_indices_from_projects(src, writer, counter):
    javafiles = java_files_from_dir(src)	#자바 파일들만 뽑아내는 함수
    i = 0
    j = 0
    for javafile in javafiles:
        i += 1
        if i % 1000 == 0:	#1000개 될때마다 프린트 한번씩
            print("Counter: %s" % i)
            #print "typed_method_call" + str(counter.typed_method_call_count)

        document = Document()	#루씬 Document 객체

        ################################################################################################################
        splits = javafile.split("/")[6:]    # Git indexing 할땐 새로 설정 아마 [5:] 였지?
        project_path = ""
        for names in splits:
            project_path += "/" + names

        changed_path = src[:-1] + project_path
        document.add(Field("file", changed_path, Field.Store.YES, Field.Index.ANALYZED))

        ################################################################################################################
        # document.add(Field("file", javafile, Field.Store.YES, Field.Index.NO))
        try:
            with codecs.open(javafile, "r", encoding='utf-8', errors='ignore') as f:
                file_content = f.read().encode("utf-8", errors='ignore')

            file_content = file_content.decode("utf8")  #
            ast = parse(file_content, resolve=False)	#newJavaParser를 사용하여 자바 코드 파싱
            # if buildDoc(document, file_content, ast, counter):                                ####### 이 부분이 Original
            if buildDocWithoutStructure(document, file_content):
                writer.addDocument(document)
                j += 1
                if j % 1000 == 0:
                    print "Wrote:: %s files" % j

        except Exception as e:
            print("Error: %s" % e)
            continue
    print "Number of files: %s" % i
    print "Number of duplicates: %s" % len(hashes)
    print "%s files has been indexed" % j



def buildDoc(document, file_content, node, counter):
    # Flag is set when at least 1 code characteristics has been stored
    flag = False
    #document.add( Field("var_type_map", str(dict(node["var_type_map"])), Field.Store.YES, Field.Index.NO))
    document.add(Field("line_numbers", str(dict(node["line_numbers"])), Field.Store.YES, Field.Index.NO))
    document.add(Field("hash", str(md5(file_content)), Field.Store.YES, Field.Index.NO))
    # Code as Text Do we still need comments ?

    # document.add(Field("code", so_tokenizer(file_content, False), Field.Store.YES, Field.Index.ANALYZED))     #
    document.add(Field("code", preProcessing(file_content, False), Field.Store.YES, Field.Index.ANALYZED))
    #루씬에서 인덱싱 할때 알아서 tokenize해줄텐데.. 왜 so_tokenizer를 사용했지 여기서??

    for m in node["typed_method_call"]:
        if m:
            document.add(Field("typed_method_call", m, Field.Store.YES, Field.Index.ANALYZED))
            counter.typed_method_call_count += 1
            flag = True

    for e in node["extends"]:
        if e:
            document.add(Field("extends", e, Field.Store.NO, Field.Index.ANALYZED))
            counter.extends_count += 1

    for c in node["used_classes"]:
        if c:
            document.add(Field("used_classes", str(c), Field.Store.YES, Field.Index.ANALYZED))
            counter.used_classes_count += 1

    for i in node["class_instance_creation"]:
        if i:
            document.add(Field("class_instance_creation", i, Field.Store.YES, Field.Index.ANALYZED))
            counter.class_instance_creation_count += 1
            flag = True

    for m in node["methods"]:
        if m:
            document.add(Field("methods", m, Field.Store.YES, Field.Index.ANALYZED))
            counter.methods_count += 1

    for m in node["methods_called"]:
        if m:
            document.add(Field("methods_called", m, Field.Store.YES, Field.Index.ANALYZED))
            counter.methods_called_count += 1
            flag = True

    for m in node["unresolved_method_calls"]:
        if m:
            document.add(Field("unresolved_method_calls", m, Field.Store.YES, Field.Index.ANALYZED))
            counter.unresolved_method_calls_count += 1

    for l in node["literals"]:
        if l:
            document.add(StringField("literals", l, Field.Store.YES))
            counter.literals_count += 1
    return flag

def buildDocWithoutStructure(document, file_content):
    if FLAG_BASELINE is True:
        # To make the baseline
        document.add(Field("code", specialCharRemove(file_content), Field.Store.YES, Field.Index.ANALYZED))
    else:
        # To make the preprocessed
        document.add(Field("code", preProcessing(file_content, False), Field.Store.YES, Field.Index.ANALYZED))

    return True

def indexingMain(src, dst):
    import time
    print '*** Indexing Project Data***\n'
    start_time = time.time()
    try:
        indicesDestination = File(dst)
        #writer = IndexWriter(SimpleFSDirectory(indexDestination), StandardAnalyzer(), True, IndexWriter.MaxFieldLength.UNLIMITED)
        #Analyzer : 본문이나 제목 등의 텍스트를 색인하기 전에 반드시 분석기를 거쳐 단어로 분리해야 한다. Analyzer 클래스는 Directory와 함께 IndexWrite 클래스의 생성 메소드에 지정하며 지정된 텍슽트를 색인할 단위 단어로 분리하고 필요 없는 단어를 제거하는 등의 역할을 담당

        analyzer = KeywordAnalyzer()  #전체 텍스트를 하나의 토큰으로 다룬다. (즉, Analyze 하지 않는 것과 결과적으로 동일하다.)
        a = {"code": JavaCodeAnalyzer(), "comments": EnglishAnalyzer(Version.LUCENE_CURRENT)} #PerFieldAnalyzerWrapper를 사용하기 위한 map 생성 (Python 에서는 Dict())
        wrapper_analyzer = PerFieldAnalyzerWrapper(analyzer, a) 				#http://svn.apache.org/viewvc/lucene/pylucene/trunk/test/test_PerFieldAnalyzerWrapper.py?revision=1757704&view=co
        config = IndexWriterConfig(Version.LUCENE_CURRENT, wrapper_analyzer)
        writer = IndexWriter(SimpleFSDirectory(indicesDestination), config)
        #SimpleFSDirectory 옵션은 파일시스템에 특정 디렉토리에 인덱스 파일을 저장하겠다. DB, RAM, File system 3개가 있음
        #config 는 IndexWriter 사용에 필요한 Analyzed 된 token이다.

        counter = Counter()
        generate_indices_from_projects(src, writer, counter)
        writer.close()

        print "Done"
        #print "--- %s seconds ---" % (time.time() - start_time)
        print str(counter)

    except CorruptIndexException as e:		#when index is corrupt
            e.printStackTrace()
    except LockObtainFailedException as e:	#when other writer is using the index
            e.printStackTrace()
    except IOException as e:	#when directory can't be read/written
            e.printStackTrace()


#####################
# FLAG_BASELINE 설정 #
#####################
FLAG_BASELINE = True

if __name__ == '__main__':
    '''Bench4BL ALL'''
    target_lits = ['Apache/Hive', 'Apache/Hbase', 'Apache/Camel',
                   'Commons/Codec', 'Commons/Collections', 'Commons/Compress', 'Commons/Configuration', 'Commons/Crypto',
                   'Commons/Csv', 'Commons/Io', 'Commons/Lang', 'Commons/Math', 'Commons/Weaver',
                   'Jboss/Entesb', 'Jboss/Jbmeta',
                   'Previous/AspectJ', 'Previous/Jdt', 'Previous/Pde', 'Previous/Swt', 'Previous/Zxing',
                   'Spring/Amqp', 'Spring/Batchadm', 'Spring/Datajpa', 'Spring/Datarest', 'Spring/Roo',
                   'Spring/Sgf', 'Spring/Social', 'Spring/Socialtw', 'Spring/Sws', 'Spring/Android',
                   'Spring/Datacmns', 'Spring/Datamongo', 'Spring/Ldap', 'Spring/Sec', 'Spring/Shdp',
                   'Spring/Socialfb', 'Spring/Spr', 'Spring/Batch', 'Spring/Datagraph', 'Spring/Dataredis',
                   'Spring/Mobile', 'Spring/Secoauth', 'Spring/Shl', 'Spring/Socialli', 'Spring/Swf',
                   'Wildfly/Ely', 'Wildfly/Swarm', 'Wildfly/Wfarq', 'Wildfly/Wfcore', 'Wildfly/Wfly', 'Wildfly/Wfmp'
                   ]

    target_lits = ['Apache/Hive'] # I'm creating the baseline for the projects.


    for idx, target in enumerate(target_lits):
        print str(idx) + '/' + str(len(target_lits)) + ' ////// ' + str(target)
        what_to_index = ''' %s Bench4BL Index ''' % target.upper()
        target_project = 'bench4bl_%s' % target.split('/')[1].lower()
        src = '/extdsk/Bench4BL/data/%s/gitrepo/' % (target.split('/')[0] + '/' + target.split('/')[1].upper())

        if FLAG_BASELINE is True:
            target_project = target_project + '_baseline'

        dst = '/home/ubuntu/Desktop/CoCaBu/GitSearch/Indices/%s_latest_keyword' % target_project

        print src
        print dst

        if not os.path.isdir(dst):
            mkdir_p(dst)
        else:
            cleanMetaPath(dst)

        print(what_to_index)
        start_time = time.time()
        indexingMain(src, dst)
        print('--- %s seconds ---' % (time.time() - start_time))












#!/usr/bin/env python
# -*- coding: utf-8 -*-

############Bug Indexing Code############
import sys
import time

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
sys.path.append("/home/ubuntu/Desktop/sqlite-jdbc-3.23.1.jar")


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

from GitSearch.MyUtils import unescape_html, tokenize, read_file, write_file_a
from Analyzer.PorterAnalyzer import PorterAnalyzer
from Analyzer.JavaCodeAnalyzer import JavaCodeAnalyzer
from Indexer.SOParser import PostParser
from Import.ImportAST import transform_body
from Indexer._Counter import Counter
from java.sql import SQLException
import time, os
from Preprocessor import preBasic, SPC, CMC, STM, SWR, postBasic, mathProcessing, getTokens
from GitSearch.MyUtils import md5, so_tokenizer, copytree, mkdir_p, cleanMetaPath
#Jython cannot read large files (1.6MB)

def index(src, writer, pp_option):
    for bug_report in os.listdir(src):
        print('\nIssue report: %s' % (bug_report))
        result_file = src + bug_report
        contents = read_file(result_file).strip()
        # exclude_list = ['LANG-279.txt', 'HIVE-10609.txt', 'HIVE-8263.txt', 'HIVE-8879.txt', 'Hive-10244.txt']

        # if bug_report in exclude_list or contents is None or contents == '':
        #     continue



        if pp_option == 'preBasic':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            title = postBasic(tokens)

            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            description = postBasic(tokens)

        elif pp_option == 'SPC':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            description = postBasic(tokens)

        elif pp_option == 'CMC':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = CMC(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = CMC(tokens)
            description = postBasic(tokens)

        elif pp_option == 'SWR':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = SWR(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = SWR(tokens)
            description = postBasic(tokens)

        elif pp_option == 'STM':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = STM(tokens)
            description = postBasic(tokens)


        elif pp_option == 'SPC_CMC':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = CMC(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = CMC(tokens)
            description = postBasic(tokens)

        elif pp_option == 'SPC_SWR':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = SWR(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = SWR(tokens)
            description = postBasic(tokens)

        elif pp_option == 'SPC_STM':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = STM(tokens)
            description = postBasic(tokens)

        elif pp_option == 'CMC_SWR':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            description = postBasic(tokens)

        elif pp_option == 'CMC_STM':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = CMC(tokens)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = CMC(tokens)
            tokens = STM(tokens)
            description = postBasic(tokens)

        elif pp_option == 'SWR_STM':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            description = postBasic(tokens)



        elif pp_option == 'SPC_CMC_SWR':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            description = postBasic(tokens)

        elif pp_option == 'SPC_CMC_STM':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = CMC(tokens)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = CMC(tokens)
            tokens = STM(tokens)
            description = postBasic(tokens)

        elif pp_option == 'SPC_SWR_STM':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            description = postBasic(tokens)




        elif pp_option == 'CMC_SWR_STM':
            title = preBasic(contents.split('\n')[0])
            tokens = getTokens(title)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            tokens = getTokens(description)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            description = postBasic(tokens)


        elif pp_option == 'SPC_CMC_SWR_STM':
            title = preBasic(contents.split('\n')[0])
            title = SPC(title)
            tokens = getTokens(title)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            title = postBasic(tokens)
            description = preBasic('\n'.join(contents.split('\n')[1:]))
            description = SPC(description)
            tokens = getTokens(description)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            description = postBasic(tokens)





        #
        # elif pp_option == 'math':
        #     title = mathProcessing(contents.split('\n')[0])
        #     description = mathProcessing(' '.join(contents.split('\n')[1:]))
        #
        # elif pp_option == 'test':
        #     title = preBasic(contents.split('\n')[0])
        #     title = SPC(title)
        #     title = getTokens(title)
        #     title = CMC(title)
        #     title = SWR(title)
        #     title = postBasic(title)
        #     description = preBasic('\n'.join(contents.split('\n')[1:]))
        #     description = SPC(description)
        #     description = getTokens(description)
        #     description = CMC(description)
        #     description = SWR(description)
        #     description = postBasic(description)

        else:
            print('Please configure the preprocessing option!!!!!')
            time.sleep(100000)

        if title == '' or title is None:
            # time.sleep(1999999)
            write_file_a('Failed_Index.txt', bug_report)
            continue

        document = Document()
        document.add(StringField("bug_id", String.valueOf(bug_report), Field.Store.YES))
        document.add(StringField("title", String.valueOf(title), Field.Store.YES))

        str = ''
        for i in set(description):
            str += i + ' '
        description_ = str.strip()

        document.add(StringField("description", String.valueOf(description_), Field.Store.YES))#, Field.Index.ANALYZED))

        try:
            writer.addDocument(document)
        except Exception as e:
            write_file_a('/home/ubuntu/Desktop/CoCaBu/index_FAIL.txt', bug_report)
            print e


def bug_main(src, dst, pp_option):
    try:
        start_time = time.time()
        #########################################  경   로  ####################################
        indexDestination = File(dst)

        #writer = IndexWriter(SimpleFSDirectory(indexDestination), StandardAnalyzer(), True, IndexWriter.MaxFieldLength.UNLIMITED)
        analyzer = PorterAnalyzer(StandardAnalyzer(Version.LUCENE_CURRENT))
        a = {	"typed_method_call": analyzer, "extends": analyzer,
                "used_classes": analyzer, "methods": analyzer,
                "class_instance_creation": analyzer, "methods_called": analyzer, "view_count" : KeywordAnalyzer(), "code_hints": JavaCodeAnalyzer() }
        wrapper_analyzer = PerFieldAnalyzerWrapper(analyzer, a)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, wrapper_analyzer)
        writer = IndexWriter(SimpleFSDirectory(indexDestination), config)

        # analyzer = PorterAnalyzer(StandardAnalyzer(Version.LUCENE_CURRENT))
        # tmp = {"typed_method_call": KeywordAnalyzer(), "extends": KeywordAnalyzer(),
        # 	 "used_classes": KeywordAnalyzer(), "methods": KeywordAnalyzer(),
        # 	 "class_instance_creation": KeywordAnalyzer(), "methods_called": KeywordAnalyzer(),
        # 	 "view_count": KeywordAnalyzer(), "code_hints": JavaCodeAnalyzer()}
        # wrapper_analyzer = PerFieldAnalyzerWrapper(analyzer, tmp)
        # config = IndexWriterConfig(Version.LUCENE_CURRENT, wrapper_analyzer)
        # writer = IndexWriter(SimpleFSDirectory(indexDestination), config)

        index(src, writer, pp_option)
        writer.commit()
        writer.close()

        print ("Done")
        print("--- %s seconds ---" % (time.time() - start_time))

    except CorruptIndexException as e:		#when index is corrupt
            e.printStackTrace()
    except LockObtainFailedException as e:	#when other writer is using the index
            e.printStackTrace()
    except IOException as e:	#when directory can't be read/written
            e.printStackTrace()
    except SQLException as e: 	#when Database error occurs
            e.printStackTrace()

if __name__ == '__main__':
    start_time = time.time()
    base_path = '/extdsk/bug_localization/input_answer/'

    '''Bench4BL ALL'''
    target_list = ['Commons/Math', 'Apache/Hive', 'Apache/Hbase', 'Apache/Camel',
                   'Commons/Codec', 'Commons/Collections', 'Commons/Compress', 'Commons/Configuration',
                   'Commons/Crypto',
                   'Commons/Csv', 'Commons/Io', 'Commons/Lang', 'Commons/Weaver',
                   'JBoss/Entesb', 'JBoss/Jbmeta',
                   'Spring/Amqp', 'Spring/Batchadm', 'Spring/Datajpa', 'Spring/Datarest', 'Spring/Roo',
                   'Spring/Sgf', 'Spring/Social', 'Spring/Socialtw', 'Spring/Sws', 'Spring/Android',
                   'Spring/Datacmns', 'Spring/Datamongo', 'Spring/Ldap', 'Spring/Sec', 'Spring/Shdp',
                   'Spring/Socialfb', 'Spring/Spr', 'Spring/Batch', 'Spring/Datagraph', 'Spring/Dataredis',
                   'Spring/Mobile', 'Spring/Secoauth', 'Spring/Shl', 'Spring/Socialli', 'Spring/Swf',
                   'Wildfly/Ely', 'Wildfly/Swarm', 'Wildfly/Wfarq', 'Wildfly/Wfcore', 'Wildfly/Wfly', 'Wildfly/Wfmp'
                   ]  ## 'Previous/AspectJ', 'Previous/Jdt', 'Previous/Pde', 'Previous/Swt', 'Previous/Zxing'

    target_list = ['JBoss/Entesb', 'JBoss/Jbmeta']
    pp_option_list = ['preBasic',
                      'SPC', 'CMC', 'SWR', 'STM', 'SPC_CMC', 'SPC_SWR', 'SPC_STM', 'CMC_SWR', 'CMC_STM', 'SWR_STM',
                      'SPC_CMC_SWR', 'SPC_CMC_STM', 'SPC_SWR_STM', 'CMC_SWR_STM', 'SPC_CMC_SWR_STM']

    # pp_option_list = ['test']

    for idx, target in enumerate(target_list):
        for idx_, pp_option in enumerate(pp_option_list):
            target_ = target.split('/')[1].lower()
            # print str(idx) + '/' + str(len(target_list)) + ' ////// ' + str(target)
            what_to_index = ''' %s - Issue Index ''' % target_.upper()
            # print(what_to_index)

            src = base_path + u'input_issue_all/%s/' % target_.upper()
            if not os.path.isdir(src):
                write_file_a('indexing_failed.txt', target_)
                continue

            index_dst_name = 'issue_%s_%s' % (target_, pp_option)
            dst = u'/home/ubuntu/Desktop/CoCaBu/GitSearch/Indices/%s' % index_dst_name

            if not os.path.isdir(dst):
                mkdir_p(dst)
            else:
                cleanMetaPath(dst)

            bug_main(src, dst, pp_option)
            print("An index is built in %s !!!" % dst)
            print("--- %s seconds ---" % (time.time() - start_time))
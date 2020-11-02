#!/usr/bin/env jython
# -*- coding: utf-8 -*-
import sys, traceback, codecs, os, time
sys.path.append(".")
sys.path.append("..")
sys.path.append("...")
sys.path.append("/home/ubuntu/Desktop/sqlite-jdbc-3.23.1.jar")
from java.io import File, StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexReader, Term
from org.apache.lucene.search import IndexSearcher, FuzzyQuery, TermQuery
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.util import Version
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.search.spans import SpanNearQuery, SpanQuery, SpanTermQuery, SpanMultiTermQueryWrapper
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.queries.function.valuesource import LongFieldSource
from org.apache.lucene.queries.function import FunctionQuery
from org.apache.lucene.queries import CustomScoreQuery
from org.apache.lucene.search import BooleanQuery
from PorterAnalyzer import PorterAnalyzer
from JavaCodeAnalyzer import JavaCodeAnalyzer
from zlib import compress, decompress
from collections import Counter, namedtuple
from GitSearch.MyUtils import remove_unified_stop_lists
from GoogleSearcher import GoogleSearcher, YandexSearcher
from DBSearcher import getAnswerDescriptions, get_db_connection, getQuestionDescriptionsAndTags
from GitSearch.MyUtils import my_stop_words, read_file, write_file_a

def retrieve_ranked_apis(question_id):
    docs = coll.find(BasicDBObject({"question_id": question_id}))
    apis = []
    for doc in docs:
        answer = doc.toMap()
        apis.append(answer["typed_method_call"])
    print apis

def tokenize_string(analyzer, string):
    result = []
    stream = analyzer.tokenStream(None, StringReader(string))
    cattr = stream.addAttribute(CharTermAttribute)
    stream.reset()
    while stream.incrementToken():
        result.append(cattr.toString())
    stream.close()
    return result

def getSpanNearQuery(analyzer, s, field="title", slop=100, inOrder=True):
    keywords = tokenize_string(analyzer, s)
    #print keywords
    spanTermQueries = [ SpanMultiTermQueryWrapper( FuzzyQuery( Term(field, keyword) ) ) for keyword in keywords]
    return SpanNearQuery( spanTermQueries, slop, inOrder)

class YandexJiraSearcher:
    def __init__(self, index_path, flag_bug_or_issue, group_project, project, dataset, flag):
        indexDir = File(index_path)
        index = SimpleFSDirectory(indexDir)
        self.reader = IndexReader.open(index)
        n_docs = self.reader.numDocs()
        self.searcher = IndexSearcher(self.reader)
        self.flag_bug_or_issue = flag_bug_or_issue
        self.group_project = group_project
        self.project = project
        self.dataset = dataset
        self.flag = flag

    def search(self, query, initial_bugid, limit=1):
        docs = []
        matched_bugs = []
        yandex = YandexSearcher(self.project)
        bug_ids = yandex.search(query)
        target_id = None

        if self.flag == 1:
            bug_id_list = [i.split('.')[0] for i in os.listdir('/extdsk/bug_localization/input_answer/input_%s/%s' % (self.dataset, self.project))]
        else:
            bug_id_list = [i.split('.')[0] for i in os.listdir('/extdsk/bug_localization/input_answer/input_%s/%s' % (self.dataset, self.group_project.upper()))] # 원래는 self.project

        ''' bug_id 가 우리가 가지고 있는 실제버그 인지, 일반 issue 인지 판단하고 실제 bug 라면, 그거 먼저 take 즉, 10개중에 6위 (1위는 query 니까)안에 실제 버그가 있으면 그거먼저 take 하고, 아니면 2위의 issue 를 take '''

        ''' Within top 10, bug priority '''
        candidate_bug = []
        candidate_issue = []
        for idx, bug_id in enumerate(bug_ids):
            if bug_id == initial_bugid:             # Check if it is initial query (discard target)
                continue
            if bug_id in bug_id_list:               # Check if it is in the bug list (potential target)
                candidate_bug.append(bug_id)
            else:
                candidate_issue.append(bug_id)

        if self.flag_bug_or_issue == 'bug':
            # Bug 에서 고르기
            for bug in candidate_bug:
                query = TermQuery(Term("bug_id", bug + '.txt'))
                topdocs = self.searcher.search(query, 1).scoreDocs
                for hit in topdocs:  # topdocs 는 객체여서 enumerate 이 안먹네..
                    doc = self.searcher.doc(hit.doc)
                    docs.append(doc)
                    print("Bug Id: %s, Title: %s" % (doc.get("bug_id"), doc.get("title")))
                    matched_bugs.append(doc.get("bug_id"))

                write_file_a('/home/ubuntu/Desktop/CoCaBu/useBRorNot.txt', str(initial_bugid))
                return docs, matched_bugs

        elif self.flag_bug_or_issue == 'issue':
            # Issue 에서 고르기
            for issue in candidate_issue:
                query = TermQuery(Term("bug_id", issue + '.txt'))
                topdocs = self.searcher.search(query, 1).scoreDocs
                for hit in topdocs:  # topdocs 는 객체여서 enumerate 이 안먹네..
                    doc = self.searcher.doc(hit.doc)
                    docs.append(doc)
                    print("Bug Id: %s, Title: %s" % (doc.get("bug_id"), doc.get("title")))          ###현재 여기서 doc.get("title") 못가져옴.....
                    matched_bugs.append(doc.get("bug_id"))

                write_file_a('/home/ubuntu/Desktop/CoCaBu/useIRorNot.txt', str(initial_bugid))
                return docs, matched_bugs


        # else:   # 해당 랭크 안에 비슷한 버그 리포트가 없다?
        #     print '\nBug report is not existing in the Top 10, we are taking issues...\n'
        #
        #     ''' Take only from issues '''
        #     # if bug_id in bug_id_list:
        #     #     continue
        #
        #     for i, bug_id in enumerate(bug_ids):
        #         if bug_id == initial_bugid:
        #             continue
        #
        #         print i, '))', bug_id
        #         query = TermQuery(Term("bug_id", bug_id.strip() + '.txt'))
        #         topdocs = self.searcher.search(query, 1).scoreDocs
        #         for hit in topdocs:	                                # topdocs 는 객체여서 enumerate 이 안먹네..
        #             doc = self.searcher.doc(hit.doc)
        #             docs.append(doc)
        #             print("Bug Id: %s, Title: %s" % (doc.get("bug_id"), doc.get("title")))
        #             matched_bugs.append(doc.get("bug_id"))

        return docs, matched_bugs		# Answer index 에서 검색하기 때문에 Answer snippet이 있는 post 만 적용

SOResultItem = namedtuple("SOResultItem", "doc score title id description")
class GoogleStackoverflowSearcher:
    def __init__(self, index_path):
        indexDir = File(index_path)
        index = SimpleFSDirectory(indexDir)
        self.reader = IndexReader.open(index)
        n_docs = self.reader.numDocs()
        self.searcher = IndexSearcher(self.reader)

    def search(self, query, limit=1):
        docs = []
        # query += " java site:stackoverflow.com"
        google = GoogleSearcher()
        so_ids = google.search(query)                               # so id or bug id
        for i, so_id in enumerate(so_ids):
            print i, '))', so_id
            query = TermQuery(Term("question_id", so_id))
            topdocs = self.searcher.search(query, 5).scoreDocs	# 여기서는 검색엔진으로 검색해서 stackoverflow post id 를 stackoverflow index 에서 찾는다..

            for hit in topdocs:	# topdocs 는 객체여서 enumerate 이 안먹네..
                doc = self.searcher.doc(hit.doc)
                docs.append(SOResultItem(doc, len(so_ids) - i, doc.get("title"), doc.get("id"), doc.get("description")) ) #len(q_ids) - i , doc.get("view_count") MAX VIEWCOUNT: 1.914.994
                print("Title: %s, Question Id: %s, Answer Id: %s" % (doc.get("title"), doc.get("id"), doc.get("answer_id")))

        print '# of Success docs: ', len(docs)
        print 'So_ids: ', so_ids
        return docs, so_ids		# Answer index 에서 검색하기 때문에 Answer snippet이 있는 post 만 적용


class StackoverflowSearcher:
    def __init__(self, index_path):
        self.index_path = index_path
        self.reader = None
        self.query = None
        self.analyzer = None
        self.load_index()

    # 1. open the index
    def load_index(self):
        indexDir = File(self.index_path)
        porter_analyzer = PorterAnalyzer( StandardAnalyzer(Version.LUCENE_CURRENT))

        a = {	"typed_method_call": KeywordAnalyzer(),
                "extends": KeywordAnalyzer(),
                "used_classes": KeywordAnalyzer(), "methods": KeywordAnalyzer(), "class_instance_creation": KeywordAnalyzer(), "id": KeywordAnalyzer(), "code": JavaCodeAnalyzer()}

        self.analyzer = PerFieldAnalyzerWrapper(porter_analyzer, a)

        index = SimpleFSDirectory(indexDir)
        self.reader = IndexReader.open(index)
        n_docs = self.reader.numDocs()
        print("Index contains %d documents." % n_docs)

    # 2. parse the query from the command line
    def parse_query(self, query_string, order_matters=True):
        query_parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, ["title", "qbody"], self.analyzer)


        if order_matters:
            # Take into account order of query terms
            base_query = getSpanNearQuery(self.analyzer, query_string)
        else:
            # Considers query keywords as bag of words
            base_query = query_parser.parse(query_string)

        #http://shaierera.blogspot.com/2013/09/boosting-documents-in-lucene.html
        boost_query = FunctionQuery( LongFieldSource("view_count"))
        self.query = CustomScoreQuery(base_query, boost_query)

        # queryparser = QueryParser(Version.LUCENE_CURRENT, "title", analyzer)
        # query = queryparser.parse(query_string)


    # 3. search the index for the query
    # We retrieve and sort all documents that match the query.
    # In tmp real application, use tmp TopScoreDocCollector to sort the hits.
    def search(self, query_string=""):
        if not self.query:
            self.parse_query(query_string)

        searcher = IndexSearcher(self.reader)
        hits = searcher.search(self.query, 5).scoreDocs

        # When ordered query does not return any result issue an query where order does not matter
        if len(hits) < 5:
            print "Order does not matter"
            self.parse_query(query_string, False)

        print "Number of hits %s " % len(hits)
        # 4. display results
        print(query_string)
        print("Found %d hits:" % len(hits))

        items = []
        api_acc = []
        for i, hit in enumerate(hits):
            doc = searcher.doc(hit.doc)

            apis = [d.stringValue() for d in doc.getFields("typed_method_call")]
            #queries.append(self.document_to_query(doc)) # hit.doc returns lucenes internal ID for the given document
            items.append(SOResultItem(doc, hit.score, doc.get("title"), doc.get("id"), doc.get("description")))
            api_acc.extend(apis)
            #retrieve_ranked_apis(doc.get("answer_id"))
            print("%d.  %s, Answer Id: %s, Method: %s, Score: %s" % (i + 1, doc.get("title"), doc.get("answer_id"), apis, hit.score))

        print Counter(api_acc).most_common(5)
        return items
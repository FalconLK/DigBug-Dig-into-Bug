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
from DBSearcher import getAnswerDescriptions, get_db_connection, getQuestionDescriptionsAndTags
from GitSearch.MyUtils import my_stop_words, write_file_a
from Preprocessor import preBasic, SPC, CMC, STM, SWR, mathProcessing, postBasic, getTokens

GithubResultItem = namedtuple("GithubResultItem", "file file_content matched_terms score so_item line_numbers doc_id")
class GitHubSearcher:
    def __init__(self, index_path, query=None):
        self.index_path = index_path
        self.reader = None
        self.query = query
        self.porter_analyzer = PorterAnalyzer( StandardAnalyzer(Version.LUCENE_CURRENT))

        self.load_index()

    def load_index(self):
        indexDir = File(self.index_path)
        a = {"code": self.porter_analyzer}
        self.analyzer = PerFieldAnalyzerWrapper(KeywordAnalyzer(), a)
        index = SimpleFSDirectory(indexDir)
        self.reader = IndexReader.open(index)
        n_docs = self.reader.numDocs()
        self.searcher = IndexSearcher(self.reader)
        # print("Index contains %d documents." % n_docs)

    def get_DF(self, field, term):
        return self.reader.docFreq(Term(field, term))

    def get_IDF(self, field, term):
        from math import log10, sqrt
        docF = self.reader.docFreq(Term(field, term))

        return log10(self.reader.numDocs() / (docF + 1)) + 1

    def get_minimum_IDF(self, docF=2):
        from math import log10, sqrt
        return log10(self.reader.numDocs() / (docF + 1)) + 1

    def document_to_query(self, doc):
        """ Given tmp document it transforms the source code related fields to tmp lucene query string"""
        query = ""
        for field in ["typed_method_call", "methods", "used_classes", "class_instance_creation", "methods_called", "annotations", "literals"]: #"used_classes", , "literals" , "extends"
            for val in doc.getFields(field):
                if val.stringValue().strip():
                    term = QueryParser.escape(val.stringValue())

                    # Filter out noisy terms
                    stoplist = ["java.lang.Object"]
                    if term not in stoplist:
                        query += "%s:%s " % (field, term)
                        # print query

        if len(doc.getFields("code_hints")) > 0:
            hints = [hint.stringValue() for hint in doc.getFields("code_hints")]
            hints_str = " ".join(hints)
            for term in hints:
                if term:
                    term = QueryParser.escape(term)
                    print "Code hint Term:", term

        return query

    def document_to_tokens(self, doc):
        """ Source code 내에서 detection 된 모든 field 들을 그냥 일반 string token 으로 반환"""
        tokens = ""
        for field in ["typed_method_call", "methods", "used_classes", "class_instance_creation", "methods_called", "annotations", "literals"]: #"used_classes", , "literals" , "extends"
            for val in doc.getFields(field):
                if val.stringValue().strip():
                    term = QueryParser.escape(val.stringValue())
                    tokens += "code:%s " % term
                    # tokens += "%s:%s " % (field, term)

        print '\n\n\n\Doc to Tokens : %s \n\n\n\n' % tokens

        return tokens

    def get_matched_keywords(self, query, docid):
        matched_terms = []
        # def _get_matched_keywords(q, matched_terms):
        # 	print type(q), matched_terms
        # 	if isinstance(q, TermQuery):
        # 		if self.searcher.explain(q, docid).isMatch():
        # 			matched_terms.append( q.getTerm().text() )
        # 	elif isinstance(q, BooleanQuery):
        # 		for query_term in query.getClauses():
        # 			_get_matched_keywords(query_term, matched_terms)
        # 			# if self.searcher.explain(query_term.getQuery(), docid).isMatch():
        # 			# 	matched_terms.append( query_term.getQuery().getTerm().text() )

        # _get_matched_keywords(query, matched_terms)


        if isinstance(query, TermQuery):
            if self.searcher.explain(query, docid).isMatch():
                matched_terms.append( query.getTerm().text() )
        elif isinstance(query, BooleanQuery):
            for query_term in query.getClauses():
                if self.searcher.explain(query_term.getQuery(), docid).isMatch():
                    matched_terms.append( query_term.getQuery().getTerm().text() )

        #print "Matched Terms: %s" % matched_terms
        return matched_terms

    def get_matched_keywords2(self, query, doc):
        matched_terms = []
        weight_expl = self.searcher.explain(query, doc).toString().split("weight(")
        for expl in weight_expl:
            if " in " in expl:
                field_val = expl.split(" in ")[0]
                #field, val = field_val.split(":")
                val = field_val.split(":")[-1]
                matched_terms.append(val)
        return matched_terms

    def code_as_text(self, so_answer_desc):
        print 'CODE AS TEXT ... /// ... '
        """ Extends tmp query by matching query keywords in source code as text"""
        dups = []
        query = ""
        for term in tokenize_string(self.porter_analyzer, self.query):
            if term:
                term = QueryParser.escape(term)
                if not str(term) in my_stop_words:
                    if not term in dups:
                        query += "code:%s " % (term)
                        dups.append(term)

        for term in tokenize_string(self.porter_analyzer, so_answer_desc):
            if term:
                term = QueryParser.escape(term)
                if not str(term) in my_stop_words:
                    if not term in dups:
                        query += "code:%s " % (term)
                        dups.append(term)

        return query

    def code_xxxx_formatter(self, str):
        dups = []
        query = ''
        for term in str.split():
            if not term in dups and len(term) > 2:
                query += 'code:%s ' % term
                dups.append(term)
        return query

    def lexical_search(self):
        """ In case no term is matching with stackoverflow we perform tmp simple lexical search on GitHub """
        github_result = []
        query = self.code_as_text().strip()
        query = QueryParser(Version.LUCENE_CURRENT, "code", self.analyzer).parse(query)
        hits = self.searcher.search(query, 10).scoreDocs
        for hit in hits:
            doc = self.searcher.doc(hit.doc)
            matched_terms = self.get_matched_keywords(query, hit.doc)

            # apis = [d.stringValue() for d in doc.getFields("typed_method_call")]

            item = GithubResultItem(doc.get("file"), decompress( doc.get("file_content") ), matched_terms, hit.score, so_item, doc.get("line_numbers"), hit.doc) # code

            github_result.append( item )

        return github_result

    def more_like_this(self, so_items):
        github_result = []
        if not so_items:
            so_items.append( SOResultItem(None, 1.0, "No Title", 0, "") )

        for so_item in so_items:
            queryparser = QueryParser(Version.LUCENE_CURRENT, "typed_method_call", self.analyzer)
            query = ""
            if so_item.doc:
                query = self.document_to_query(so_item.doc)

            query += self.code_as_text()
            if query:
                print "-"*30
                print "Query: %s" % query
                print "-"*30
                try:
                    like_query = queryparser.parse(query)
                    hits = self.searcher.search(like_query, 10).scoreDocs

                    for i, hit in enumerate(hits):
                        doc = self.searcher.doc(hit.doc)
                        matched_terms = self.get_matched_keywords2(like_query, hit.doc)

                        # apis = [d.stringValue() for d in doc.getFields("typed_method_call")]
                        item = GithubResultItem(doc.get("file"), decompress( doc.get("file_content") ), matched_terms, hit.score, so_item, doc.get("line_numbers"), hit.doc) # code

                        github_result.append(item)
                        #print("%d. File: %s, Matched: %s, Score: %s" % (i + 1, doc.get("file"), matched_terms, hit.score))
                except Exception as e:
                    print "Error: %s" % e

        return github_result

    def more_like_this2(self, so_items):
        # result_path = '/home/ubuntu/Desktop/CoCaBu/results.txt'
        # if os.path.isfile(result_path):
        # 	os.remove(result_path)
        github_result = []
        if not so_items:
            so_items.append(SOResultItem(None, 1.0, "No Title", 0, ""))

        for so_item in so_items:
            print type(so_item)
            query = ""
            queryparser = QueryParser(Version.LUCENE_CURRENT, "typed_method_call", self.analyzer)
            if so_item.doc:
                query += self.document_to_query(so_item.doc)
            query += self.code_as_text()

            if query:
                print '' * 2
                print "-" * 100
                print "<<< Final Query and Results >>>"
                print "-" * 100
                print "UNified Query: %s" % query
                print "-" * 100
                try:
                    query = remove_unified_stop_lists(query)
                    print 'After removing stop words: ', query
                    like_query = queryparser.parse(query)
                    hits = self.searcher.search(like_query, 20000).scoreDocs

                    for i, hit in enumerate(hits):
                        doc = self.searcher.doc(hit.doc)
                        matched_terms = self.get_matched_keywords2(like_query, hit.doc)

                        # apis = [d.stringValue() for d in doc.getFields("typed_method_call")]
                        # print("file__", doc.get("file"), "file_content", doc.get("file_content"), "line_numbers", doc.get("line_numbers") )
                        file_path = '/'.join(str(doc.get("file")).split('/')[:5]) + '/' + '/'.join(str(doc.get("file")).split('/')[7:])
                        # print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', file_path
                        # write_file_a(result_path, str(file_path))

                        content = None
                        try:
                            with open(file_path) as f:
                                content = f.read()
                        except:
                            pass

                        if content:
                            item = GithubResultItem(doc.get("file"), content, matched_terms, hit.score, so_item, doc.get("line_numbers"), hit.doc) # code
                            github_result.append(item)
                        #print("%d. File: %s, Matched: %s, Score: %s" % (i + 1, doc.get("file"), matched_terms, hit.score))

                except Exception as e:
                    print "GitSearcher: Error: %s" % e
                    print(traceback.format_exc())

        # print Counter(files).most_common(5)
        return github_result

    def bugdoc_to_tokens(self, doc):
        tokens = ""
        token_list = []
        bug_id = doc.get("bug_id")
        title = doc.get("title")
        description = doc.get("description")
        print 'Taking ', bug_id, '...................'

        for token in title.split():
            token_list.append("code:%s" % token)
            tokens += "code:%s" % token + ' '
        # for token in description.split():
        #     token_list.append("code:%s" % token)
        #     tokens += "code:%s" % token + ' '

        # without_dups = ' '.join([str(i) for i in list(set(token_list))])
        with_dups = tokens

        return with_dups  #Bug report 내에 description token이 상당히 길고, 중복되는 경우가 많기 때문에 여기선 set 을 테스트해보자.



















    def more_like_this2_without_html(self, middle_items, result_path, so_ids, pp_option):
        '''Unified query (all 10 stack answers in tmp query)'''
        result_dict = dict()
        # db_conn = get_db_connection()

        ########################################################################################################
        ############################################ Query part ################################################
        ########################################################################################################

        # Adding initial query
        file_content = self.query
        print('&' * 100, pp_option)
        print(file_content)

        if pp_option == 'preBasic':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            file_content = postBasic(tokens)

        elif pp_option == 'SPC':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            file_content = postBasic(tokens)
            # file_content = ' '.join(tokens)

        elif pp_option == 'CMC':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'SWR':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = SWR(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'STM':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = STM(tokens)
            file_content = postBasic(tokens)


        elif pp_option == 'SPC_CMC':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            # nonDigit = [i for i in tokens if (not i.isdigit())]
            # file_content = ' '.join(nonDigit)
            file_content = postBasic(tokens)

        elif pp_option == 'SPC_SWR':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = SWR(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'SPC_STM':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = STM(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'CMC_SWR':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'CMC_STM':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            tokens = STM(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'SWR_STM':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            file_content = postBasic(tokens)


        elif pp_option == 'SPC_CMC_SWR':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'SPC_CMC_STM':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            tokens = STM(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'SPC_SWR_STM':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'CMC_SWR_STM':
            file_content = preBasic(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            file_content = postBasic(tokens)

        elif pp_option == 'SPC_CMC_SWR_STM':
            file_content = preBasic(file_content)
            file_content = SPC(file_content)
            tokens = getTokens(file_content)
            tokens = CMC(tokens)
            tokens = SWR(tokens)
            tokens = STM(tokens)
            file_content = postBasic(tokens)

        # elif pp_option == 'math':
        #     file_content = mathProcessing(file_content)
        #
        # elif pp_option == 'test':
        #     file_content = preBasic(file_content)
        #     file_content = SPC(file_content)
        #     # print file_content
        #     tokens = getTokens(file_content)
        #     file_content = CMC(tokens)
        #     file_content = SWR(file_content)
        #     file_content = postBasic(file_content)

        else:
            print('Please configure the preprocessing option!!!!!')
            time.sleep(100000)


        # initial_query = pp_option(initial_query)
        # initial_query = specialCharRemove(initial_query)
        print file_content
        initial_query = self.code_xxxx_formatter(file_content)

        # Adding answer or question descriptions here
        so_a_desc_query = ''
        so_q_desc_query = ''

        cnt = 0
        # for id in so_ids:
        #     if cnt == 1:                                                    # Top 1 stackoverflow description ################################################
        #         break
        #     so_a_desc_query += getAnswerDescriptions(id, db_conn) + ' '     # Answer description
        #     desc, tags = getQuestionDescriptionsAndTags(id, db_conn)        # Question description
        #     so_q_desc_query += desc
        #     cnt += 1
        #     print 'DB success %s..' % cnt

        # processed_so_a_desc_query = preProcessing(so_a_desc_query)
        # processed_so_q_desc_query = preProcessing(so_q_desc_query)
        # so_q_desc_query = self.code_xxxx_formatter(processed_so_q_desc_query)
        # so_a_desc_query = self.code_xxxx_formatter(processed_so_a_desc_query)

        # Adding answer snippets here
        so_a_snippet_query = ''
        # for item in middle_items:
        #     so_a_snippet_query += self.document_to_tokens(item.doc) + ' '    #Structured query? or Simple keyword matching between SO and PROJECT?




        '''Yandex similar posts'''
        # bug_query = ''
        # for item in middle_items:
        #     bug_query += self.bugdoc_to_tokens(item) + ' '
        #     break   #  break 를 걸면 상위 1개의 bug item에 대해서만 query 를 만든다.






        ############# Select the method (Replace? Augment?) ################################################################################################
        ''' Stackoerflow Query Part '''
        # final_tokens = initial_query                                                      # Only initial query
        # final_tokens = so_q_desc_query                                                    # Replace to so question description
        # final_tokens = so_a_desc_query                                                    # Replace to so answer description
        # final_tokens = so_a_snippet_query                                                 # Replace to so answer snippet

        # final_tokens = initial_query + ' ' + so_q_desc_query                              # Combination (initial + so_q_desc)
        # final_tokens = initial_query + ' ' + so_a_desc_query                              # Combination (initial + so_a_desc)
        # final_tokens = initial_query + ' ' + so_a_snippet_query                           # Combination (initial + so_a_snippet)

        # final_tokens = so_q_desc_query + ' ' + so_a_desc_query                            # Combination (so_q_desc + so_a_desc)
        # final_tokens = so_q_desc_query + ' ' + so_a_snippet_query                         # Combination (so_q_desc + so_a_snippet)
        # final_tokens = so_a_desc_query + ' ' + so_a_snippet_query                         # Combination (so_a_desc + so_a_snippet)

        # final_tokens = initial_query + ' ' + so_q_desc_query + ' ' + so_a_desc_query              # Combination (initial + so_q_desc + so_a_desc)
        # final_tokens = initial_query + ' ' + so_q_desc_query + ' ' + so_a_snippet_query           # Combination (initial + so_q_desc + so_a_snippet)
        # final_tokens = initial_query + ' ' + so_a_desc_query + ' ' + so_a_snippet_query           # Combination (initial + so_a_desc + so_a_snippet)
        # final_tokens = so_q_desc_query + ' ' + so_a_desc_query + ' ' + so_a_snippet_query         # Combination (so_q_desc + so_a_desc + so_a_snippet)

        # final_tokens = initial_query + ' ' + so_q_desc_query + ' ' + so_a_desc_query + ' ' + so_a_snippet_query      # Combination (initial + so_q_desc + so_a_desc + so_a_snippet)

        ''' Bug Query Part '''
        '''Summary to Summary (Bug-Summary > YandexSimBug-Summary)'''

        '''1'''
        final_tokens = initial_query

        '''2'''
        # final_tokens = initial_query + bug_query

        '''3'''
        # if bug_query:
        #     final_tokens = initial_query + bug_query
        # else:
        #     final_tokens = initial_query

        ############## Query parser setting [Is this tmp code token matching? or just tmp key word matching?] ##############
        if final_tokens == so_a_snippet_query:
            queryparser = QueryParser(Version.LUCENE_CURRENT, "typed_method_call", self.analyzer)       # Code element matching
        else:
            queryparser = QueryParser(Version.LUCENE_CURRENT, "code", self.analyzer)                    # Keyword matching

        ############## If there is no final tokens (No SO? then Initial query)
        # if final_tokens == '' or final_tokens is None:
        #     final_tokens = initial_query
        #     queryparser = QueryParser(Version.LUCENE_CURRENT, "code", self.analyzer)

        ############## If there is no final tokens then, return
        if final_tokens == '' or final_tokens is None:
            # time.sleep(10000000)
            return

        ########################################################################################################
        ########################################################################################################
        ########################################################################################################

        print '' * 2
        print "-" * 100
        print "<<< Query Processing... >>>"
        print "-" * 100
        print "Initial Query: %s" % initial_query
        print "-" * 100
        query = remove_unified_stop_lists(final_tokens)
        print "UNified Query: %s" % query
        print "-" * 100
        try:
            like_query = queryparser.parse(query)
            hits = self.searcher.search(like_query, 20000).scoreDocs

            for i, hit in enumerate(hits):
                doc = self.searcher.doc(hit.doc)

                matched_terms = self.get_matched_keywords2(like_query, hit.doc)

                file_path = '/'.join(str(doc.get("file")).split('/')[:5]) + '/' + '/'.join(str(doc.get("file")).split('/')[7:])
                # print '////////////////////////////////////////File PATH: ', file_path

                result_file = file_path.split('/')[-1]

                result_dict.update({result_file: hit.score})


                # Print the retrieved files [RESULTS]
                if i < 10:
                    print("%d. File: %s, Matched: %s, Score: %s" % (i + 1, doc.get("file"), matched_terms, hit.score))
                    write_file_a('/extdsk/results/%s' % result_path.split('/')[-1], str(doc.get("file")) + str(matched_terms))

        except Exception as e:
            print "GitSearcher: Error: %s" % e
            print(traceback.format_exc())

        # ranking and saving the results
        sorted_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
        result_list = []
        for tup in sorted_dict:
            if not tup[0] in result_list:
                result_list.append(tup[0])
                # print str(tup[0])
                # import time
                # time.sleep(1000000000)
                write_file_a(result_path, str(tup[0]))

        # print Counter(files).most_common(5)
        print '# of Results: ', len(result_list)















    '''Stackoverflow 고려안함'''
    def more_like_this2_without_html_and_augmentation(self, result_path):
        print '****^^^^^^ %s ^^^^^^******' % result_path

        result_dict = dict()

        # Transform ("code:xxxx")
        initial_query = self.query
        initial_query = specialCharRemove(initial_query)
        final_query = self.code_xxxx_formatter(initial_query)
        queryparser = QueryParser(Version.LUCENE_CURRENT, "code", self.analyzer)

        print '' * 2
        print "-" * 100
        print "<<< Final Query and Results >>>"
        print "-" * 100
        print "UNified Query: %s" % final_query
        print "-" * 100
        try:
            like_query = queryparser.parse(final_query)
            hits = self.searcher.search(like_query, 20000).scoreDocs

            for i, hit in enumerate(hits):
                doc = self.searcher.doc(hit.doc)
                matched_terms = self.get_matched_keywords2(like_query, hit.doc)

                # apis = [d.stringValue() for d in doc.getFields("typed_method_call")]
                # print("file__", doc.get("file"), "file_content", doc.get("file_content"), "line_numbers", doc.get("line_numbers") )
                file_path = '/'.join(str(doc.get("file")).split('/')[:5]) + '/' + '/'.join(str(doc.get("file")).split('/')[7:])
                # print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', file_path
                result_file = file_path.split('/')[-1]
                result_dict.update({result_file: hit.score})

                # content = None
                # try:
                # 	with open(file_path) as f:
                # 		content = f.read()
                # except:
                # 	pass
                #
                # if content:
                # 	item = GithubResultItem(doc.get("file"), content, matched_terms, hit.score, so_item, doc.get("line_numbers"), hit.doc) # code
                # 	github_result.append(item)

                # if i < 10:
                #     print("%d. File: %s, Matched: %s, Score: %s" % (i + 1, doc.get("file"), matched_terms, hit.score))

        except Exception as e:
            print "GitSearcher: Error: %s" % e
            print(traceback.format_exc())

        # ranking and saving the results
        sorted_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
        result_list = []
        for tup in sorted_dict:
            if not tup[0] in result_list:
                result_list.append(tup[0])
                write_file_a(result_path, str(tup[0]))

        # print Counter(files).most_common(5)
        return None

if __name__ == '__main__':
    # so = StackoverflowSearcher("/Users/Raphael/Downloads/stackoverflow")
    # so_items = so.search("messageformat receive tmp stack trace")

    # git = GitHubSearcher("/Users/Raphael/Downloads/github")
    # git.more_like_this(so_items)

    porter_analyzer = PorterAnalyzer( StandardAnalyzer(Version.LUCENE_CURRENT))
    print tokenize_string(porter_analyzer, "Convert and Int to String")

#!/usr/bin/env jython
#-*- coding: utf-8 -*-
# sys.setrecursionlimit(800000)

from flask import Flask, Markup, render_template, send_from_directory, request
from GitSearchItem import GitSearchItem
from GitSearchResult import GitSearchResult
from GitSearchFile import highlight_file
from GitSearcher import GitHubSearcher
from MiddleSearcher import YandexJiraSearcher, GoogleStackoverflowSearcher
from collections import namedtuple
from utils import read_file
from highlight import highlight_files
import traceback, codecs, os
from time import time
import gc

# TODO: Query Index
# TODO: Ranking
# open files and highlight
# TODO: Return results back to user

# INDEX_BASE_PATH = "/home/ubuntu/Desktop/CoCaBu/GitSearch/Indices/" #"/Users/Raphael/Downloads/"

# DigBug
INDEX_BASE_PATH = "/home/ubuntu/Desktop/CoCaBu/GitSearch/Indices/bench4bl_original/" #"/Users/Raphael/Downloads/"


'''
jython -J-Xmx12288m Bootstrap.py FrontEnd/server.py

12GB: 12288
8GB: 8192
'''


############################### Application Start ###############################
app = Flask(__name__, static_folder='static')
def to_q(path):
    from urllib import quote_plus
    return quote_plus(path)

app.jinja_env.globals.update(to_q=to_q)

def write_file_a(file_path, content):
    with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
        file.write(content + "\n")

@app.route("/", methods=['GET', 'POST'])	#allow both GET and POST requests
def index(name=None):
    if request.method == 'POST':
        print '**********************************************************************************************************************'
        print '**********************************************************************************************************************'
        print '**********************************************************************************************************************'
        query = request.form['key']

        target = str(str(query).split('$$')[0])
        result_file = str(str(query).split('$$')[1])
        pp_option = str(str(query).split('$$')[2])
        query = str('$$'.join(str(query).split('$$')[3:]))

        flag = 1

        ############################### Which Dataset and Project? ###############################
        dataset = 'bench4bl'
        project = target.split('/')[1]

        # dataset = 'ifixr'   #
        # project = target    #
        group_project = ''

        ############################### Select Stackoverflow Index ###############################
        # STACK_INDEX_TO_USE = 'stackoverflow_full_desc'

        ############################### Select Report Index ######################################
        # REPORT_INDEX_TO_USE = '%s_bug' % project.lower()
        REPORT_INDEX_TO_USE = 'issue_%s_%s' % (project.lower(), pp_option)
        print 'Report Index: ', REPORT_INDEX_TO_USE


        ############################### Select Project Index #####################################
        PROJECT_INDEX_TO_USE = '%s_%s_%s' % (dataset, project.lower(), pp_option)
        print 'Project Index: ', PROJECT_INDEX_TO_USE

        ############################### Using bug? or Issue? #####################################
        BUG_or_ISSUE = REPORT_INDEX_TO_USE.split('_')[0]


        github_items = None
        try:
            if query:
                #1
                # github_items = query_index(query)															#Original
                # so_result = query_index_without_html(query, result_file, PROJECT_INDEX_TO_USE, PROJECT_INDEX_TO_USE)
                so_result = query_index_without_html(query, result_file, REPORT_INDEX_TO_USE, PROJECT_INDEX_TO_USE, BUG_or_ISSUE, group_project, project, dataset, flag, pp_option)
                print '\n' *20
                if so_result is False:
                    return
                # query_index_without_html_and_augmentation(query, result_file)

                # 2
                # if github_items:
                # 	git_search_result = GitSearchResult(github_items)
                # git_search_result = ''
                # return render_template("search.html", name=query, git_search_result=git_search_result)
        except:
            print(traceback.format_exc())

    else:
        query = request.args.get('q')
        print query
        result_file = str(str(query).split('$$')[0])
        query = str(str(query).split('$$')[1])

        github_items = None
        try:
            if query:
                # 1
                # github_items = query_index(query)															#Original
                # so_result = query_index_without_html(query, result_file)
                # so_result = query_index_without_html(query, result_file, REPORT_INDEX_TO_USE, PROJECT_INDEX_TO_USE, flag_bug_or_issue, project, dataset)
                print '\n' * 20
                if so_result is False:
                    return
                # query_index_without_html_and_augmentation(query, result_file)

                # 2
                # if github_items:
                #     git_search_result = GitSearchResult(github_items)
                git_search_result = ''
                return render_template("search.html", name=query, git_search_result=git_search_result)
        except:
            print(traceback.format_exc())

    return render_template("index.html", name=name)








# @app.route("/")
# def index(name=None):
# 	print '(((((((((((((((((((GET))))))))))))))))))))'
# 	query = request.args.get('q')
# 	evaluation = request.args.get("evaluation")
# 	print query
# 	result_file = str(str(query).split('$$')[0])
# 	query = str(str(query).split('$$')[1])
#
# 	github_items = None
# 	try:
# 		if query:
# 			if evaluation:
# 				github_items = query_index2(query)
# 			else:
# 				# 1
# 				# github_items = query_index(query)															#Original
# 				# query_index_without_html(query, result_file)
# 				query_index_without_html_and_augmentation(query, result_file)
#
# 			# 2
# 			if github_items:
# 				git_search_result = GitSearchResult(github_items)
#
# 			return render_template("search.html", name=query, git_search_result=git_search_result)
# 	except:
# 		print(traceback.format_exc())
#
# 	return render_template("index.html", name=name)


@app.route('/source')
def show_source():
    file_path = request.args.get('q')
    if file_path:
        html = highlight_file(file_path)
        return render_template("file.html", file_path=file_path, source = html)

@app.route('/<path:file_path>')
def static_proxy(file_path):
    # send_static_file will guess the correct MIME type
    return send_from_directory(app.static_folder, file_path)

def render_code_results(query):
    github_items = query_index(query)
    git_search_items = [ GitSearchItem(github_item) for github_item in github_items ]
    return git_search_items

def query_index(query):
    # Getting the Stackoverflow Items
    t = time()
    google_so = GoogleStackoverflowSearcher("%sstackoverflow_C" % (INDEX_BASE_PATH)) #
    so_items = google_so.search(query, 5)
    print "\n\n# of Stackoverflow items: ", len(so_items)
    print "\n\nGoogle Stackoverflow Search Request Time: %s" % (time()-t)

    # Getting the Gihub Items
    t = time()
    github = GitHubSearcher("%scamel" % (INDEX_BASE_PATH), query)
    github_items = github.more_like_this2(so_items)
    print "\n\n# of Code base items: ", len(github_items)
    print "\n\nCode base index request time: %s" % (time()-t)

    return github_items

def logging(so_ids, so_items, result_file):
    '''아래 로그파일들은 여기서 자동으로 지우면 안된다.'''
    so_fail_log_file = '/home/ubuntu/Desktop/CoCaBu/so_fail.txt'
    so_success_log_file = '/home/ubuntu/Desktop/CoCaBu/so_success.txt'
    if so_ids is None or so_ids == '':
        print
        'SO_FAILED//'
        write_file_a(so_fail_log_file, result_file)
        return False
    else:
        print
        'SO_SUCCEED//'
        write_file_a(so_success_log_file, result_file + '$$' + str(len(so_items)))

def query_index_without_html(query, result_file, REPORT_INDEX_TO_USE, PROJECT_INDEX_TO_USE, flag_bug_or_issue, group_project, project, dataset, flag, pp_option):
    # GOOGLE
    # google_so = GoogleStackoverflowSearcher("%s%s" % (INDEX_BASE_PATH, STACK_INDEX_TO_USE))
    # so_items, so_ids = google_so.search(query, 5)

    '''Yandex Similar Posts'''
    so_items = ''
    so_ids = ''
    # initial_bugid = result_file.split('/')[-1].split('.')[0]
    # yandex_jira = YandexJiraSearcher("%s%s" % (INDEX_BASE_PATH, REPORT_INDEX_TO_USE), flag_bug_or_issue, group_project, project, dataset, flag)
    # so_items, so_ids = yandex_jira.search(query, initial_bugid, 5)

    '''logging 이 enable 이면, middle result 없을시 진행 멈춤'''
    # logging(so_ids, so_items, result_file)

    # Getting the Gihub Items
    t = time()
    print 'GITHUB SEARCHER// Query: ', query
    github = GitHubSearcher("%s%s" % (INDEX_BASE_PATH, PROJECT_INDEX_TO_USE), query)
    print 'Going into the more like this func.., pp option: %s' % pp_option
    github.more_like_this2_without_html(so_items, result_file, so_ids, pp_option)

    # print "\n\n# of Code base items: ", len(github_items)
    print "\n\nCode base index request time: %s" % (time()-t)
    return True




'''Stackoverflow 고려안함'''
def query_index_without_html_and_augmentation(query, result_file):
    t = time()
    github = GitHubSearcher("%s%s" % (INDEX_BASE_PATH, PROJECT_INDEX_TO_USE), query)
    github_items = github.more_like_this2_without_html_and_augmentation(result_file)

    print "\n\n# of Code base items: ", len(github_items)
    print "\n\nCode base index request time: %s" % (time()-t)







def query_index2(query):
    """ Returns tmp set of file paths relevant to given query """
    print "Evaluation Index"
    from time import time
    t = time()
    google = GoogleStackoverflowSearcher("%sevaluation201306" % (INDEX_BASE_PATH)) #
    so_items = google.search(query, 10)
    print "Google Request Time: %s" % (time()-t)
    t = time()

    github = GitHubSearcher("%sgithub" % (INDEX_BASE_PATH), query)
    github_items = github.more_like_this(so_items)

    print "GitSearch Request Time: %s" % (time()-t)
    return github_items

if __name__ == "__main__":
    while True:
        try:
            app.run(host="0.0.0.0", port=4569)
            # app.run(host="0.0.0.0", port=6600)
        except Exception as e:
            print e


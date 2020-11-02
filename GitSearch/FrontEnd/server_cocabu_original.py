#!/usr/bin/env jython
#-*- coding: utf-8 -*-
# sys.setrecursionlimit(800000)

import sys
sys.path.append('.')
sys.path.append('..')
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
from GitSearch.MyUtils import write_file_a

# TODO: Query Index
# TODO: Ranking
# open files and highlight
# TODO: Return results back to user

INDEX_BASE_PATH = "/home/ubuntu/Desktop/CoCaBu/GitSearch/Indices/" #"/Users/Raphael/Downloads/"

'''
jython -J-Xmx12288m Bootstrap.py server.py

12GB: 12288
8GB: 8192
'''

############################### Application Start ###############################
app = Flask(__name__, static_folder='static')
def to_q(path):
    from urllib import quote_plus
    return quote_plus(path)

app.jinja_env.globals.update(to_q=to_q)

@app.route("/")
def index(name=None):
    query = request.args.get('q')
    try:
        if query:
            # 1
            github_items = query_index(query)															#Original

            print 'How many github items: ', len(github_items)

            # 2
            if github_items:
                git_search_result = GitSearchResult(github_items)

            return render_template("search.html", name=query, git_search_result=git_search_result)
    except:
        print(traceback.format_exc())

    return render_template("index.html", name=name)

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

    # for i in so_items:
    #     print i

    print "\n\nGoogle Stackoverflow Search Request Time: %s" % (time()-t)
    print '--------------------------------------------------------'

    # Getting the Gihub Items
    t = time()
    github = GitHubSearcher("%sgithub" % (INDEX_BASE_PATH), query)
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

def query_index_without_html(query, result_file, REPORT_INDEX_TO_USE, PROJECT_INDEX_TO_USE, flag_bug_or_issue, group_project, project, dataset, flag):
    GOOGLE
    google_so = GoogleStackoverflowSearcher("%s%s" % (INDEX_BASE_PATH, STACK_INDEX_TO_USE))
    so_items, so_ids = google_so.search(query, 5)

    '''logging 이 enable 이면, middle result 없을시 진행 멈춤'''
    logging(so_ids, so_items, result_file)

    # Getting the Gihub Items
    t = time()
    print 'GITHUB SEARCHER//'
    github = GitHubSearcher("%s%s" % (INDEX_BASE_PATH, PROJECT_INDEX_TO_USE), query)
    github.more_like_this2_without_html(so_items, result_file, so_ids)

    # print "\n\n# of Code base items: ", len(github_items)
    print "\n\nCode base index request time: %s" % (time()-t)
    return True

if __name__ == "__main__":
    while True:
        try:
            app.run(host="0.0.0.0", port=4568)
        except Exception as e:
            print e


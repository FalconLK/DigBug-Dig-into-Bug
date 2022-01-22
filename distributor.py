#-*- coding: utf-8 -*-
# from __future__ import print_function
from os.path import join
import pickle
import gzip, logging, sys, os, csv, time
sys.path.append('.')
sys.path.append('..')
from utils import mkdir_p, write_file_a, read_file, cleanMetaPath, load_zipped_pickle, getClassNames
from os.path import join, isfile
import sys, glob, os, xml, codecs
from bs4 import BeautifulSoup as Soup
every_counter = 0
cn_counter = 0
def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file
def SplitReportsToBuckets(target_list, input_bug_list, stack_trace_lst, output_path, target):
    every_cnt = 0
    target_cnt = 0
    os.chdir('path')
    with open("file.pickle", "rb") as f:
        bench_bug_dev_user = pickle.load(f)
    bug_list = list()
    bug_isDeveloper_dict = dict()
    base = 'path' % (target.split('/')[0], target.split('/')[-1].upper())
    for xml_file in os.listdir(base):
        flag = 0    # Did the report get into any bucket?
        every_cnt += 1
        # print(base + xml_file)
        handler = open(base + xml_file).read()
        soup = Soup(handler, features='lxml')
        for item in soup.findAll('item'):
            title = str(item.find('title').string)
            bug = title.split('[')[1].split(']')[0]
            if not bug in input_bug_list:
                continue
            target_cnt += 1
            summary = str(item.find('summary').string)
            description = str(item.find('description').string)
            status = str(item.find('status').string)
            reporter = str(item.find('reporter').string)
            created_date = str(item.find('created').string)
            dev_user = bench_bug_dev_user[bug]
            attachment = str(item.find('attachments').string)
            ''' Set feature values '''
            f_dev_user = 'user'
            f_attachment = 'attach_x'
            f_summary = 'summary_x'
            f_classname = 'class_x'
            f_desc = 'desc_x'
            f_stacktrace = 'stack_x'
            if not summary is None:
                f_summary = 'summary_o'
                class_file = 'path' + 'path' + 'file.txt' % target.split('/')[-1].capitalize()
                class_names = getClassNames(class_file)
                for class_name in class_names:
                    if class_name.split('/')[-1] in summary:
                        f_classname = 'class_o'
                        break
            if dev_user == True:
                f_dev_user = 'developer'
            if not attachment == 'None':
                f_attachment = 'attach_o'
            if not description is None:
                f_desc = 'desc_o'
                if bug in stack_trace_lst:
                    f_stacktrace = 'stack_o'
            if f_classname == 'class_o':
                if f_dev_user == 'developer':
                    if f_attachment == 'attach_o':
                        if f_desc == 'desc_o':
                            if f_stacktrace == 'stack_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_stacktrace == 'stack_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_desc == 'desc_x':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                    elif f_attachment == 'attach_x':
                        if f_stacktrace == 'stack_o':
                            if f_summary == 'summary_o':
                                if f_desc == 'desc_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_stacktrace == 'stack_x':
                            if f_desc == 'desc_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_desc == 'desc_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                elif f_dev_user == 'user':
                    if f_stacktrace == 'stack_o':
                        if f_attachment == 'attach_o':
                            if f_summary == 'summary_o':
                                if f_desc == 'desc_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_summary == 'summary_o':
                                if f_desc == 'desc_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                    elif f_stacktrace == 'stack_x':
                        if f_attachment == 'attach_o':
                            if f_desc == 'desc_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_desc == 'desc_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_desc == 'desc_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_desc == 'desc_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
            elif f_classname == 'class_x':
                if f_dev_user == 'developer':
                    if f_desc == 'desc_o':
                        if f_attachment == 'attach_o':
                            if f_stacktrace == 'stack_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_stacktrace == 'stack_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_stacktrace == 'stack_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_stacktrace == 'stack_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                    elif f_desc == 'desc_x':
                        if f_attachment == 'attach_o':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                elif f_dev_user == 'user':
                    if f_desc == 'desc_o':
                        if f_stacktrace == 'stack_o':
                            if f_attachment == 'attach_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_attachment == 'attach_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_stacktrace == 'stack_x':
                            if f_attachment == 'attach_o':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                            elif f_attachment == 'attach_x':
                                if f_summary == 'summary_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                    elif f_desc == 'desc_x':
                        if f_attachment == 'attach_o':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_o':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    flag = 1
                                    print(bug, '\t')
                                    write_file_a(output_path + 'file.txt', bug)
                                    continue
            if flag == 0:
                write_file_a(output_path + 'file.txt', bug)

if __name__ == "__main__":
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
                   ]
    input_bug_list = list()
    input_path = 'path'
    exe_dir = "path"
    os.chdir(exe_dir)
    stack_trace_lst = []
    for target in target_list:
        for report in os.listdir(input_path + target.split('/')[-1]):
            print('Checking.. %s' % report)
            input_bug_list.append(report.split('.')[0])
            info_target = input_path + target.split('/')[-1] + '/' + report
            if isfile(info_target + '.cleaned'):
                os.remove(info_target + '.cleaned')
            if isfile(info_target + '.result.xml'):
                os.remove(info_target + '.result.xml')
            a = os.popen("/opt/gradle/gradle-6.1/bin/gradle run -s --args='%s'" % info_target).read()
            for line in a.split('\n'):
                if 'Stack Traces' in line:
                    if int(line[0]) > 0:
                        stack_trace_lst.append(report.split('.')[0])
                        write_file_a('info_stack.txt', report.split('.')[0])
                        print('%s: Marked as true' % report.split('.')[0])
            if isfile(info_target + '.cleaned'):
                os.remove(info_target + '.cleaned')
            if isfile(info_target + '.result.xml'):
                os.remove(info_target + '.result.xml')
    for idx, target in enumerate(target_list):
        output_path = 'path' % target.split('/')[-1]
        if os.path.isdir(output_path):
            cleanMetaPath(output_path)
        else:
            mkdir_p(output_path)
        SplitReportsToBuckets(target_list, input_bug_list, stack_trace_lst, output_path, target)

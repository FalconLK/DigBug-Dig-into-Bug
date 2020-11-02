#-*- coding: utf-8 -*-
import pickle
import gzip, sys
sys.path.append('.')
sys.path.append('..')
from GitSearch.MyUtils import mkdir_p, write_file_a, read_file, cleanMetaPath
import os
from bs4 import BeautifulSoup as Soup

cocabu_path = '/home/ubuntu/Desktop/CoCaBu/'

every_counter = 0
cn_counter = 0

def getClassNames(class_name_file):
    class_names = list()
    classes_contents = read_file(class_name_file)
    for line in classes_contents.splitlines():
        class_names.append(line.split('.')[0])
    return class_names

def loadZippedPickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        return loaded_object

def splitReportsToBuckets(target_list, input_bug_list, output_path, target):
    every_cnt = 0
    target_cnt = 0

    with open("bench_bug_dev_user.pickle", "rb") as f:
        bench_bug_dev_user = pickle.load(f)

    bug_list = list()
    bug_isDeveloper_dict = dict()

    base = '/extdsk/Bench4BL/data/%s/%s/bugrepo/bugs/' % (target.split('/')[0], target.split('/')[-1].upper())
    for xml_file in os.listdir(base):
        flag = 0    # Did the report get into any bucket?
        every_cnt += 1
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
            label_localizable = 'impossible'
            '''Summary is existing?'''
            if not summary is None:
                f_summary = 'summary_o'
                '''Does the summary have class names?'''
                # Run Javaparser to get the class names
                class_file = cocabu_path + 'DecisionTree_Bench4BL/class_names_per_project/' + 'classes_%s.txt' % target.split('/')[-1].capitalize()
                class_names = getClassNames(class_file)
                for class_name in class_names:
                    if class_name.split('/')[-1] in summary:
                        f_classname = 'class_o'
                        break

            '''Reporter and Committer is the same person?'''
            if dev_user == True:
                f_dev_user = 'developer'
            '''Does the report have attachments?'''
            if not attachment == 'None':
                f_attachment = 'attach_o'
            '''Description is existing?'''
            if not description is None:
                f_desc = 'desc_o'
                '''Does the description have stack traces?'''
                if 'org.apache.' in description:
                    f_stacktrace = 'stack_o'
            if f_classname == 'class_o':
                if f_dev_user == 'developer':
                    if f_attachment == 'attach_o':
                        if f_desc == 'desc_o':
                            if f_stacktrace == 'stack_o':
                                if f_summary == 'summary_o':
                                    '#1'
                                    flag = 1
                                    print(bug, '\t#1')
                                    write_file_a(output_path + '1.txt', bug)
                                    continue
                            elif f_stacktrace == 'stack_x':
                                if f_summary == 'summary_o':
                                    '#2'
                                    flag = 1
                                    print(bug, '\t#2')
                                    write_file_a(output_path + '2.txt', bug)
                                    continue
                        elif f_desc == 'desc_x':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    '#3'
                                    flag = 1
                                    print(bug, '\t#3')
                                    write_file_a(output_path + '3.txt', bug)
                                    continue
                    elif f_attachment == 'attach_x':
                        if f_stacktrace == 'stack_o':
                            if f_summary == 'summary_o':
                                if f_desc == 'desc_o':
                                    '#4'
                                    flag = 1
                                    print(bug, '\t#4')
                                    write_file_a(output_path + '4.txt', bug)
                                    continue
                        elif f_stacktrace == 'stack_x':
                            if f_desc == 'desc_o':
                                if f_summary == 'summary_o':
                                    '#5'
                                    flag = 1
                                    print(bug, '\t#5')
                                    write_file_a(output_path + '5.txt', bug)
                                    continue
                            elif f_desc == 'desc_x':
                                if f_summary == 'summary_o':
                                    '#6'
                                    flag = 1
                                    print(bug, '\t#6')
                                    write_file_a(output_path + '6.txt', bug)
                                    continue
                elif f_dev_user == 'user':
                    if f_stacktrace == 'stack_o':
                        if f_attachment == 'attach_o':
                            if f_summary == 'summary_o':
                                if f_desc == 'desc_o':
                                    '#7'
                                    flag = 1
                                    print(bug, '\t#7')
                                    write_file_a(output_path + '7.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_summary == 'summary_o':
                                if f_desc == 'desc_o':
                                    '#8'
                                    flag = 1
                                    print(bug, '\t#8')
                                    write_file_a(output_path + '8.txt', bug)
                                    continue
                    elif f_stacktrace == 'stack_x':
                        if f_attachment == 'attach_o':
                            if f_desc == 'desc_o':
                                if f_summary == 'summary_o':
                                    '#9'
                                    flag = 1
                                    print(bug, '\t#9')
                                    write_file_a(output_path + '9.txt', bug)
                                    continue
                            elif f_desc == 'desc_x':
                                if f_summary == 'summary_o':
                                    '#10'
                                    flag = 1
                                    print(bug, '\t#10')
                                    write_file_a(output_path + '10.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_desc == 'desc_o':
                                if f_summary == 'summary_o':
                                    '#11'
                                    flag = 1
                                    print(bug, '\t#11')
                                    write_file_a(output_path + '11.txt', bug)
                                    continue
                            elif f_desc == 'desc_x':
                                if f_summary == 'summary_o':
                                    '#12'
                                    flag = 1
                                    print(bug, '\t#12')
                                    write_file_a(output_path + '12.txt', bug)
                                    continue

            elif f_classname == 'class_x':
                if f_dev_user == 'developer':
                    if f_desc == 'desc_o':
                        if f_attachment == 'attach_o':
                            if f_stacktrace == 'stack_o':
                                if f_summary == 'summary_o':
                                    '#13'
                                    flag = 1
                                    print(bug, '\t#13')
                                    write_file_a(output_path + '13.txt', bug)
                                    continue
                            elif f_stacktrace == 'stack_x':
                                if f_summary == 'summary_o':
                                    '#14'
                                    flag = 1
                                    print(bug, '\t#14')
                                    write_file_a(output_path + '14.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_stacktrace == 'stack_o':
                                if f_summary == 'summary_o':
                                    '#15'
                                    flag = 1
                                    print(bug, '\t#15')
                                    write_file_a(output_path + '15.txt', bug)
                                    continue
                            elif f_stacktrace == 'stack_x':
                                if f_summary == 'summary_o':
                                    '#16'
                                    flag = 1
                                    print(bug, '\t#16')
                                    write_file_a(output_path + '16.txt', bug)
                                    continue
                    elif f_desc == 'desc_x':
                        if f_attachment == 'attach_o':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    '#17'
                                    flag = 1
                                    print(bug, '\t#17')
                                    write_file_a(output_path + '17.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    '#18'
                                    flag = 1
                                    print(bug, '\t#18')
                                    write_file_a(output_path + '18.txt', bug)
                                    continue
                elif f_dev_user == 'user':
                    if f_desc == 'desc_o':
                        if f_stacktrace == 'stack_o':
                            if f_attachment == 'attach_o':
                                if f_summary == 'summary_o':
                                    '#19'
                                    flag = 1
                                    print(bug, '\t#19')
                                    write_file_a(output_path + '19.txt', bug)
                                    continue
                            elif f_attachment == 'attach_x':
                                if f_summary == 'summary_o':
                                    '#20'
                                    flag = 1
                                    print(bug, '\t#20')
                                    write_file_a(output_path + '20.txt', bug)
                                    continue
                        elif f_stacktrace == 'stack_x':
                            if f_attachment == 'attach_o':
                                if f_summary == 'summary_o':
                                    '#21'
                                    flag = 1
                                    print(bug, '\t#21')
                                    write_file_a(output_path + '21.txt', bug)
                                    continue
                            elif f_attachment == 'attach_x':
                                if f_summary == 'summary_o':
                                    '#22'
                                    flag = 1
                                    print(bug, '\t#22')
                                    write_file_a(output_path + '22.txt', bug)
                                    continue
                    elif f_desc == 'desc_x':
                        if f_attachment == 'attach_o':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_o':
                                    '#23'
                                    flag = 1
                                    print(bug, '\t#23')
                                    write_file_a(output_path + '23.txt', bug)
                                    continue
                        elif f_attachment == 'attach_x':
                            if f_summary == 'summary_o':
                                if f_stacktrace == 'stack_x':
                                    '#24'
                                    flag = 1
                                    print(bug, '\t#24')
                                    write_file_a(output_path + '24.txt', bug)
                                    continue
            if flag == 0:
                print(bug, '#25 -------')
                write_file_a(output_path + '25.txt', bug)
    print('Everything: ', every_cnt)
    print('Target: ', target_cnt)

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
    input_path = '/extdsk/bug_localization/input_answer/input_bench4bl/'
    for target in target_list:
        for report in os.listdir(input_path + target.split('/')[-1]):
            input_bug_list.append(report.split('.')[0])
    for idx, target in enumerate(target_list):
        print('-'*200)
        print('Project: ', target)
        output_path = '/home/ubuntu/Desktop/CoCaBu/DigBug/buckets/%s/' % target.split('/')[-1]
        if os.path.isdir(output_path):
            cleanMetaPath(output_path)
        else:
            mkdir_p(output_path)
        print('Output path: %s', output_path)
        splitReportsToBuckets(target_list, input_bug_list, output_path, target)

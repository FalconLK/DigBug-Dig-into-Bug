#-*- coding: utf-8 -*-
import pickle
import gzip, sys, os
sys.path.append('.')
sys.path.append('..')
from utils import mkdir_p, write_file_a, read_file, cleanMetaPath, load_zipped_pickle
from bs4 import BeautifulSoup as Soup
from collections import defaultdict
base_path = 'path'
every_counter = 0
cn_counter = 0
def getClassNames(class_name_file):
    class_names = list()
    classes_contents = read_file(class_name_file)
    for line in classes_contents.splitlines():
        class_names.append(line.split('.')[0])
    return class_names
def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object
def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


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
            # info_target = input_path + target.split('/')[-1] + '/' + report
            #
            # if isfile(info_target + '.cleaned'):
            #     os.remove(info_target + '.cleaned')
            # if isfile(info_target + '.result.xml'):
            #     os.remove(info_target + '.result.xml')
            #
            # a = os.popen("/opt/gradle/gradle-6.1/bin/gradle run -s --args='%s'" % info_target).read()
            # for line in a.split('\n'):
            #     if 'Stack Traces' in line:
            #         if int(line[0]) > 0:
            #             stack_trace_lst.append(report.split('.')[0])
            #             write_file_a('info_stack.txt', report.split('.')[0])
            #             print('%s: Marked as true' % report.split('.')[0])
            #         else:
            #             pass
            #         continue
            #
            # if isfile(info_target + '.cleaned'):
            #     os.remove(info_target + '.cleaned')
            # if isfile(info_target + '.result.xml'):
            #     os.remove(info_target + '.result.xml')
    attr_dict = defaultdict(int)
    for idx, target in enumerate(target_list):
        print('Project: ', target)
        output_path = 'path' % target.split('/')[-1]
        # if os.path.isdir(output_path):
        #     cleanMetaPath(output_path)
        # else:
        #     mkdir_p(output_path)
        # print('Output path: %s' % output_path)
        # unique_valid_bugs = [i for i in read_file(data_path + 'hunk_available_unique_bugs.txt').splitlines()]
    print(attr_dict)

# 'stack' : 1137,
# 'user': 6948,
# 'desc': 9459,
# 'code': 5191,
# 'attach': 6210,
# 'developer': 2511

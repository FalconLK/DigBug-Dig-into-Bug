#-*- coding: utf-8 -*-
import sys, os, xml, codecs
from bs4 import BeautifulSoup as Soup
from GitSearch.MyUtils import mkdir_p, write_file, cleanMetaPath

cocabu_path = os.path.dirname(os.path.abspath(__file__)) + '/'

def generateInputAndAnswerSplitByVersion(target, source_version, soup, input_path_base, features):
    for bug in soup.findAll('bug'):
        file_list = list()
        bug_id = str(bug['id'])
        version_only = str(source_version.split('.')[0])

        summary = str(bug.find('summary').string)
        description = str(bug.find('description').string)
        for file in bug.findAll('file'):
            file_list.append(file.string)

        # Print bug report info
        print (version_only)
        print ('\t' + bug_id)
        print ('\t\t' + str(features))
        print ('\t\t\t' + str(file_list))

        # Generating the inputs
        input_path = input_path_base + version_only + '/'
        if not os.path.isdir(input_path):
            mkdir_p(input_path)

        for feature in features:
            if feature == 'summary':
                write_file(input_path + bug_id + '.txt', summary)
            if feature == 'description':
                write_file(input_path + bug_id + '.txt', description)

        ###### Generating the answers
        answer_path = cocabu_path + 'input_answer/answer_bench4bl/%s/' % target + version_only + '/'
        if not os.path.isdir(answer_path):
            mkdir_p(answer_path)
        for file in file_list:
            file_name = '.'.join(str(file).split('.')[-2:])
            write_file(answer_path + bug_id + '.txt', file_name)

def generateInputAndAnswer(target, source_version, soup, input_path_base, answer_path_base, features):
    for bug in soup.findAll('bug'):
        file_list = list()
        bug_id = str(bug['id'])
        version_only = str(source_version.split('.')[0])

        summary = str(bug.find('summary').string)
        description = str(bug.find('description').string)
        for file in bug.findAll('file'):
            file_list.append(file.string)

        # Print bug report info
        print (version_only)
        print ('\t' + bug_id)
        print ('\t\t' + str(features))
        print ('\t\t\t' + str(file_list))

        # Generating the inputs
        for feature in features:
            if feature == 'summary':
                write_file(input_path_base + target.upper() + '-' + bug_id + '.txt', summary)
            if feature == 'description':
                write_file(input_path_base + target.upper() + '-' + bug_id + '.txt', description)

        ###### Generating the answers
        for file in file_list:
            file_name = '.'.join(str(file).split('.')[-2:])
            write_file(answer_path_base + target.upper() + '-' + bug_id + '.txt', file_name)

def clearPath(output_path):
    if os.path.isdir(output_path):
        cleanMetaPath(output_path)
    else:
        mkdir_p(output_path)

if __name__ == "__main__":
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

    for idx, target in enumerate(target_list):
        src = '/extdsk/Bench4BL/data/%s/bugrepo/repository/' % (target.split('/')[0] + '/' + target.split('/')[1].upper())

        target = target.split('/')[1]
        features = ['summary', 'description']

        input_path_base = '/extdsk/bug_localization/' + 'input_answer/input_bench4bl/%s/' % target
        answer_path_base = '/extdsk/bug_localization/' + 'input_answer/answer_bench4bl/%s/' % target

        clearPath(input_path_base)
        clearPath(answer_path_base)

        for root, dirs, files in os.walk(src):
            for source_version_xml in files:
                handler = open(src + source_version_xml).read()
                soup = Soup(handler)
                # generateInputAndAnswerSplitByVersion(target, source_version_xml, soup, input_path_base, features)
                generateInputAndAnswer(target, source_version_xml, soup, input_path_base, answer_path_base, features)
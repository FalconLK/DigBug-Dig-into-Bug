import os
from os.path import join, isfile
import gzip, logging, sys, os, csv, time, datetime
import pickle as p
sys.path.append('.')
sys.path.append('..')
from GitSearch.MyUtils import mkdir_p, write_file_a, read_file
from DigBug.TARGETS import total_whole_list, total_localizable_list
current_path = os.path.dirname(os.path.abspath(__file__)) + '/'


print(1)

''' 
[Every projects] 
'DATAREDIS', 'ANDROID', 'MOBILE', 'HIVE', 'ROO', 'ENTESB', 'AMQP', 'LDAP', 'COLLECTIONS', 'SPR', 'WFCORE', 
'LANG', 'SEC', 'WFARQ', 'CODEC', 'SOCIALTW', 'DATACMNS', 'MATH', 'DATAREST', 'SGF', 'DATAGRAPH', 'CSV', 'JBMETA', 
'COMPRESS', 'SECOAUTH', 'SWARM', 'HBASE', 'CRYPTO', 'BATCH', 'SWS', 'SOCIALFB', 'SHL', 'WEAVER', 'WFLY', 'ELY', 
'SWF', 'SOCIALLI', 'DATAMONGO', 'IO', 'CAMEL', 'WFMP', 'BATCHADM', 'CONFIGURATION', 'SHDP', 'DATAJPA', 'SOCIAL'
'''

project_list = ['hive', 'hbase', 'camel', 'commons-lang', 'commons-math', 'commons-codec', 'commons-collections',
                    'commons-compress', 'commons-configuration', 'commons-io', 'spring-batch', 'spring-amqp']



def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        return loaded_object

def getClassNames(class_name_file):
    class_names = list()
    classes_contents = read_file(class_name_file)
    for line in classes_contents.splitlines():
        class_names.append(line.split('.')[0])
    return class_names


def mergeTables():
    for project in project_list:
        with open(current_path + 'decision_tables/decision_table_%s.csv' % project, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)


def builder(project):
    #"""bugReport / summary / description / open / updated / reporterDN / reporterEmail / hasAttachment / attachmentTime / hasPR / commentsCount / project / bid / committerEmail / sameEmail / type / dev or user"""
    pickle_base = '/extdsk/iFixR/data/pickles/'
    issue_pickle_path = pickle_base + 'ALLbugReportsComplete_new.pickle'
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):


            ''' FEATURES / summary / description / dev_user / class_name / stack_trace / attachments / '''
            ''' Set feature values '''
            f_dev_user = 'user'
            f_attachment = 'attach_x'
            f_summary = 'summary_x'
            f_classname = 'class_x'
            f_desc = 'desc_x'
            f_stacktrace = 'stack_x'
            label_localizable = 'impossible'


            every_cnt += 1
            bid = df.iloc[idx]['bid']
            reporter = df.iloc[idx]['bid']
            type = df.iloc[idx]['type']
            if bid.split('-')[0] == project.split('-')[-1].upper() and type == 'Bug':
                target_cnt += 1
                # print(bid)
            else:
                continue


            # if type == 'Bug':
            #     target_cnt += 1
            # else:
            #     continue


            # summary = df.iloc[idx]['summary']
            # description = df.iloc[idx]['description']
            # # project_ = df.iloc[idx]['project']
            # dev_user = df.iloc[idx]['isDeveloper']
            # reporter_email = df.iloc[idx]['reporterEmail']
            # resolved = int(df.iloc[idx]['resolved'].split('-')[0])
            #
            # open_year = int(df.iloc[idx]['created'].split('-')[0])  # 2013
            # open_date = str(df.iloc[idx]['created'].split('T')[0])  # 2013-09-07
            # open_date_ = time.strptime(open_date, "%Y-%m-%d")
            #
            # attachment = df.iloc[idx]['hasAttachment']
            # if attachment:
            #     attachment_time = str(df.iloc[idx]['attachmentTime'][:19].replace('T', '-').replace(':', '-')) # 2013-09-07T18:30:00
            #     att_year = int(attachment_time.split('-')[0])
            #     att_month = int(attachment_time.split('-')[1])
            #     att_day = int(attachment_time.split('-')[2])
            #     att_hour = int(attachment_time.split('-')[3])
            #     att_min = int(attachment_time.split('-')[4])
            #     att_sec = int(attachment_time.split('-')[5])
            #     att = datetime.datetime(att_year, att_month, att_day, att_hour, att_min, att_sec)
            #
            #     open_time = str(df.iloc[idx]['created'][:19].replace('T', '-').replace(':', '-')) # 2013-09-07T18:30:00
            #     open_year = int(open_time.split('-')[0])
            #     open_month = int(open_time.split('-')[1])
            #     open_day = int(open_time.split('-')[2])
            #     open_hour = int(open_time.split('-')[3])
            #     open_min = int(open_time.split('-')[4])
            #     open_sec = int(open_time.split('-')[5])
            #     open_ = datetime.datetime(open_year, open_month, open_day, open_hour, open_min, open_sec)
            #
            #     if att == open_:  # Attachment 는 동일한 타이밍에 제출된 attachment 만 허가됨.
            #         attachment_date = str(df.iloc[idx]['attachmentTime'].split('T')[0])  # 2013-09-07
            #         attachment_time_ = time.strptime(attachment_date, "%Y-%m-%d")
            #         '''Does the report have attachments?'''
            #         f_attachment = 'attach_o'


            # if not bid in total_whole_list:
            #     continue

    print(project)
    # print('# of Everything: ', every_cnt)
    print('# of Target: ', target_cnt)




def printLocalizableProjects():
    pickle_base = '/extdsk/iFixR/data/pickles/'
    issue_pickle_path = pickle_base + 'top10localizable.pickle' # 19600 in total
    every_cnt = 0
    project_set = set()
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            every_cnt += 1
            bid = df.iloc[idx]['bid']
            yes_or_no = df.iloc[idx]['localizable']

            project = bid.split('-')[0]
            project_set.add(project)


    print(project_set)

def getLocalizableReports(intersection_projects):
    pickle_base = '/extdsk/iFixR/data/pickles/'
    issue_pickle_path = pickle_base + 'top10localizable.pickle' # 19600 in total
    every_cnt = 0
    target_report_list = list()
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            every_cnt += 1
            bid = df.iloc[idx]['bid']
            yes_or_no = df.iloc[idx]['localizable']

            project = bid.split('-')[0]
            if project in intersection_projects:
                target_report_list.append(bid)
                write_file_a('target_reports_train.txt', bid)

    return target_report_list


if __name__ == "__main__":

    project_list = ['hive', 'hbase', 'camel', 'commons-lang', 'commons-math', 'commons-codec', 'commons-collections',
                    'commons-compress', 'commons-configuration', 'commons-io', 'spring-batch', 'spring-amqp']

    project_list = ['DATAREDIS', 'ANDROID', 'MOBILE', 'HIVE', 'ROO', 'ENTESB', 'AMQP', 'LDAP', 'COLLECTIONS', 'SPR', 'WFCORE',
    'LANG', 'SEC', 'WFARQ', 'CODEC', 'SOCIALTW', 'DATACMNS', 'MATH', 'DATAREST', 'SGF', 'DATAGRAPH', 'CSV', 'JBMETA',
    'COMPRESS', 'SECOAUTH', 'SWARM', 'HBASE', 'CRYPTO', 'BATCH', 'SWS', 'SOCIALFB', 'SHL', 'WEAVER', 'WFLY', 'ELY',
    'SWF', 'SOCIALLI', 'DATAMONGO', 'IO', 'CAMEL', 'WFMP', 'BATCHADM', 'CONFIGURATION', 'SHDP', 'DATAJPA', 'SOCIAL']

    for idx, project in enumerate(project_list):
        builder(project)

    # getLocalizableReports()
    project_list_2 = ['SEC', 'WFCORE', 'LDAP', 'SOCIALTW', 'WICKET', 'AMQP', 'ACCUMULO', 'COMPRESS', 'DATAREST', 'ENTESB', 'MOBILE', 'CODEC', 'SWARM', 'SWS', 'WEAVER', 'SOCIAL', 'JBMETA', 'ROO', 'DATAMONGO', 'CAMEL', 'SECOAUTH', 'BATCHADM', 'COLLECTIONS', 'SWF', 'DATAGRAPH', 'IO', 'HBASE', 'ANDROID', 'WFMP', 'SOCIALFB', 'WFARQ', 'LOG4J2', 'DATAREDIS', 'ELY', 'MNG', 'HIVE', 'CSV', 'CONFIGURATION', 'OAK', 'SPR', 'SHDP', 'BATCH', 'SGF', 'CRYPTO', 'FLINK', 'DATAJPA', 'DATACMNS', 'WFLY', 'SOCIALLI']

    # print(set(project_list) & set(project_list_2))

    intersection = ['DATAREDIS', 'WFLY', 'COLLECTIONS', 'WFARQ', 'JBMETA', 'AMQP', 'WEAVER', 'SGF', 'SWARM', 'DATAREST', 'SOCIALLI', 'MOBILE', 'CODEC', 'COMPRESS', 'SHDP', 'SPR', 'DATAJPA', 'SOCIALTW', 'ENTESB', 'DATAGRAPH', 'LDAP', 'CRYPTO', 'SECOAUTH', 'BATCH', 'HBASE', 'SWS', 'CSV', 'DATAMONGO', 'DATACMNS', 'ANDROID', 'IO', 'SOCIAL', 'WFMP', 'SEC', 'ELY', 'HIVE', 'SOCIALFB', 'CONFIGURATION', 'CAMEL', 'ROO', 'WFCORE', 'BATCHADM', 'SWF']

    # target_reports = getLocalizableReports(intersection)





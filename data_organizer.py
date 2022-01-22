from os.path import join, isfile
import gzip, sys, os, csv, time, datetime
import pickle as p
sys.path.append('.')
sys.path.append('..')
from utils import mkdir_p, write_file_a, read_file
current_path = os.path.dirname(os.path.abspath(__file__)) + '/'
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
        with open(current_path + 'path' % project, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
def printLocalizableProjects():
    pickle_base = 'path'
    issue_pickle_path = pickle_base + 'file_path'
    every_cnt = 0
    project_set = set()
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            every_cnt += 1
            bid = df.iloc[idx]['bid']
            project = bid.split('-')[0]
            project_set.add(project)
    print(project_set)
def getTrainingReportsFromPickle(intersection_projects):
    pickle_base = 'path'
    issue_pickle_path = pickle_base + 'file_path'
    every_cnt = 0
    project_set = set()
    if os.path.isfile('file_path'):
        os.remove('file_path')
    full_target_report_list = list()
    target_report_list = list()
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            every_cnt += 1
            bid = df.iloc[idx]['bid']
            project = bid.split('-')[0]
            project_set.add(project)
            full_target_report_list.append(bid)
            if project in intersection_projects:
                target_report_list.append(bid)
                write_file_a('file_path', bid)
    return target_report_list
def getDictBidLoc():
    bid_loc_dict = dict()
    pickle_base = 'path'
    issue_pickle_path = pickle_base + 'file_path'
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            bid = df.iloc[idx]['bid']
            yes_or_no = df.iloc[idx]['localizable']
            bid_loc_dict[bid] = yes_or_no
    return bid_loc_dict
def getBenchReportList():
    bench_reports= list()
    bench_base = 'path'
    for bench_project in os.listdir(bench_base):
        project_path = bench_base + bench_project
        for report in os.listdir(project_path):
            bench_reports.append(report.split('.txt')[0])
    return bench_reports
def discardBenchFromIfixer(training_reports_ifixer, bench_reports):
    total_number = 0
    discard_number = 0
    target_number = 0
    final_training_list = list()
    for ifixr_report in training_reports_ifixer:
        total_number += 1
        if ifixr_report in bench_reports:
            discard_number += 1
            continue
        else:
            target_number += 1
            final_training_list.append(ifixr_report)
    return final_training_list, total_number, discard_number, target_number
def tableBuilder(final_training_list, localizable_list, result_file, project):
    pickle_base = 'path'
    issue_pickle_path = pickle_base + 'path.pickle'
    target_cnt = 0
    every_cnt = 0
    header = ['localize', 'dev_user', 'attachment', 'summary', 'class', 'desc', 'stack']
    if os.path.isfile(result_file):
        os.remove(result_file)
    results_fp = open(current_path + result_file, 'tmp')
    results_writer = csv.writer(results_fp, delimiter=',')
    results_writer.writerow(i for i in header)
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            label_localizable = 'impossible'
            every_cnt += 1
            bid = df.iloc[idx]['bid']
            summary = df.iloc[idx]['summary']
            description = df.iloc[idx]['description']
            # project_ = df.iloc[idx]['project']
            dev_user = df.iloc[idx]['isDeveloper']
            reporter_email = df.iloc[idx]['reporterEmail']
            resolved = int(df.iloc[idx]['resolved'].split('-')[0])
            open_year = int(df.iloc[idx]['created'].split('-')[0])
            open_date = str(df.iloc[idx]['created'].split('T')[0])
            open_date_ = time.strptime(open_date, "%Y-%m-%d")
            attachment = df.iloc[idx]['hasAttachment']
            if attachment:
                attachment_time = str(df.iloc[idx]['attachmentTime'][:19].replace('T', '-').replace(':', '-'))
                att_year = int(attachment_time.split('-')[0])
                att_month = int(attachment_time.split('-')[1])
                att_day = int(attachment_time.split('-')[2])
                att_hour = int(attachment_time.split('-')[3])
                att_min = int(attachment_time.split('-')[4])
                att_sec = int(attachment_time.split('-')[5])
                att = datetime.datetime(att_year, att_month, att_day, att_hour, att_min, att_sec)
                open_time = str(df.iloc[idx]['created'][:19].replace('T', '-').replace(':', '-'))
                open_year = int(open_time.split('-')[0])
                open_month = int(open_time.split('-')[1])
                open_day = int(open_time.split('-')[2])
                open_hour = int(open_time.split('-')[3])
                open_min = int(open_time.split('-')[4])
                open_sec = int(open_time.split('-')[5])
                open_ = datetime.datetime(open_year, open_month, open_day, open_hour, open_min, open_sec)
                if att == open_:
                    attachment_date = str(df.iloc[idx]['attachmentTime'].split('T')[0])
                    attachment_time_ = time.strptime(attachment_date, "%Y-%m-%d")
    results_fp.close()

if __name__ == "__main__":
    bench_project_list = [
        'DATAREDIS', 'ANDROID', 'MOBILE', 'HIVE', 'ROO', 'ENTESB', 'AMQP', 'LDAP', 'COLLECTIONS', 'SPR', 'WFCORE',
        'LANG', 'SEC', 'WFARQ', 'CODEC', 'SOCIALTW', 'DATACMNS', 'MATH', 'DATAREST', 'SGF', 'DATAGRAPH', 'CSV', 'JBMETA',
        'COMPRESS', 'SECOAUTH', 'SWARM', 'HBASE', 'CRYPTO', 'BATCH', 'SWS', 'SOCIALFB', 'SHL', 'WEAVER', 'WFLY', 'ELY',
        'SWF', 'SOCIALLI', 'DATAMONGO', 'IO', 'CAMEL', 'WFMP', 'BATCHADM', 'CONFIGURATION', 'SHDP', 'DATAJPA', 'SOCIAL'
    ]
    printLocalizableProjects()
    ifix_project_list = [
        'SEC', 'WFCORE', 'LDAP', 'SOCIALTW', 'WICKET', 'AMQP', 'ACCUMULO', 'COMPRESS', 'DATAREST', 'ENTESB', 'MOBILE',
        'CODEC', 'SWARM', 'SWS', 'WEAVER', 'SOCIAL', 'JBMETA', 'ROO', 'DATAMONGO', 'CAMEL', 'SECOAUTH', 'BATCHADM',
        'COLLECTIONS', 'SWF', 'DATAGRAPH', 'IO', 'HBASE', 'ANDROID', 'WFMP', 'SOCIALFB', 'WFARQ', 'LOG4J2', 'DATAREDIS',
        'ELY', 'MNG', 'HIVE', 'CSV', 'CONFIGURATION', 'OAK', 'SPR', 'SHDP', 'BATCH', 'SGF', 'CRYPTO', 'FLINK', 'DATAJPA',
        'DATACMNS', 'WFLY', 'SOCIALLI'
    ]
    project_intersection = [
        'DATAREDIS', 'WFLY', 'COLLECTIONS', 'WFARQ', 'AMQP', 'SWARM', 'DATAREST', 'SOCIALLI',
        'MOBILE', 'CODEC', 'COMPRESS', 'DATAJPA', 'SOCIALTW', 'LDAP', 'CRYPTO',
        'SECOAUTH', 'BATCH', 'HBASE', 'CSV', 'DATAMONGO', 'DATACMNS', 'ANDROID', 'IO', 'SOCIAL', 'WFMP', 'SEC',
        'ELY', 'HIVE', 'SOCIALFB', 'CONFIGURATION', 'CAMEL', 'ROO', 'WFCORE', 'BATCHADM'
    ]
    training_reports_ifixer = getTrainingReportsFromPickle(project_intersection)
    bench_reports = getBenchReportList()
    final_training_list, total_number, discard_number, target_number = discardBenchFromIfixer(training_reports_ifixer, bench_reports)
    bug_loc_dict = getDictBidLoc()
    project_list = ['spring-data-redis', 'wildfly', 'commons-collections', 'wildfly-arquillian', 'spring-amqp', 'wildfly-swarm',
                    'spring-data-rest', 'spring-social-linkedin', 'spring-mobile', 'commons-codec', 'commons-compress',
                    'spring-data-jpa', 'spring-social-twitter', 'spring-ldap', 'commons-crypto',
                    'spring-security-oauth', 'spring-batch', 'hbase', 'commons-csv', 'spring-data-mongodb',
                    'spring-data-commons', 'spring-android', 'commons-io', 'spring-social', 'wildfly-maven-plugin',
                    'spring-security', 'wildfly-elytron', 'hive', 'spring-social-facebook', 'commons-configuration',
                    'camel', 'spring-roo', 'wildfly-core', 'spring-batch-admin'
                    ]
    project_mapping = dict()
    for idx, i in enumerate(project_intersection):
        project_mapping[i] = project_list[idx]
    total_list = list()
    total_localizable_list = list()
    total_unlocalizable_list = list()
    for project in project_intersection:
        integrated_list = list()
        localizable_list = list()
        unlocalizable_list = list()
        for report in final_training_list:
            if report.split('-')[0] == project:
                localizability = bug_loc_dict[report]
                integrated_list.append(report)
                if localizability == True:
                    localizable_list.append(report)
                else:
                    unlocalizable_list.append(report)
        total_list.append(integrated_list)
        total_localizable_list.append(localizable_list)
        total_unlocalizable_list.append(unlocalizable_list)
    for idx, project in enumerate(project_list):
        output_file = 'file.csv' % project
        if os.path.isfile(output_file): os.remove(output_file)
        tableBuilder(total_list[idx], total_localizable_list[idx], total_unlocalizable_list[idx], output_file, project)

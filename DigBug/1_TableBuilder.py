import os
from os.path import join, isfile
import gzip, logging, sys, os, csv, time, datetime
import pickle as p
sys.path.append('.')
sys.path.append('..')
from GitSearch.MyUtils import mkdir_p, write_file_a, read_file
from TARGETS import total_whole_list, total_localizable_list
current_path = os.path.dirname(os.path.abspath(__file__)) + '/'

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


def builder(total_whole_list, total_localizable_list, result_file, project):
    ''' Building decision tables for each target project '''
    pickle_base = '/extdsk/iFixR/data/pickles/'
    issue_pickle_path = pickle_base + 'ALLbugReportsComplete_new.pickle'

    target_cnt = 0
    every_cnt = 0

    header = ['localize', 'dev_user', 'attachment', 'summary', 'class', 'desc', 'stack']
    if os.path.isfile(result_file):
        os.remove(result_file)
    results_fp = open(current_path + result_file, 'tmp')
    results_writer = csv.writer(results_fp, delimiter=',')
    results_writer.writerow(i for i in header)

    print('**' * 20 + project + '**' * 20)

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
            summary = df.iloc[idx]['summary']
            description = df.iloc[idx]['description']
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
                    '''Does the report have attachments?'''
                    f_attachment = 'attach_o'


            if not bid in total_whole_list:
                continue
            target_cnt += 1
            print(target_cnt)

            '''Reporter and Committer is the same person?'''
            if dev_user == 1:
                f_dev_user = 'developer'


            '''Summary is existing?'''
            if not summary is None:
                f_summary = 'summary_o'
                '''Does the summary have class names?'''
                class_info_path = current_path + 'classes_per_project/' + 'classes_%s.txt' % project.lower()
                class_names = getClassNames(class_info_path)
                for class_name in class_names:
                    if class_name in summary:
                        f_classname = 'class_o'
                        break

            '''Description is existing?'''
            if not description is None:
                f_desc = 'desc_o'
                '''Does the description have stack traces?'''
                if 'org.apache.' in description:
                    f_stacktrace = 'stack_o'

            '''Label'''
            if bid in total_localizable_list:
                label_localizable = 'possible'

            final_str = str(label_localizable) + ',' + str(f_dev_user) + ',' + str(f_attachment) + ',' + str(f_summary) + ',' + str(f_classname) + ',' + str(f_desc) + ',' + str(f_stacktrace)
            print(final_str)

            results_writer.writerow([label_localizable, f_dev_user, f_attachment, f_summary, f_classname, f_desc, f_stacktrace])

    results_fp.close()
    print('# of Everything: ', every_cnt)
    print('# of Target: ', target_cnt)


if __name__ == "__main__":
    project_list = ['hive', 'hbase', 'camel', 'commons-lang', 'commons-math', 'commons-codec', 'commons-collections',
                    'commons-compress', 'commons-configuration', 'commons-io', 'spring-batch', 'spring-amqp']

    for lst in total_whole_list:
        for ele in lst:
            write_file_a('target_projects.txt', ele)


    for idx, project in enumerate(project_list):
        output_file = 'decision_tables/decision_table_%s.csv' % project
        if os.path.isfile(output_file): os.remove(output_file)

        builder(total_whole_list[idx], total_localizable_list[idx], output_file, project)

    mergeTables()
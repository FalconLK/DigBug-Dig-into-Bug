from os.path import join, isfile
import sys, os, time
sys.path.append('.')
sys.path.append('..')
from utils import load_zipped_pickle
from TARGETS import total_whole_list, total_localizable_list
from collections import defaultdict
current_path = os.path.dirname(os.path.abspath(__file__)) + '/'

def trainTest(total_whole_list, total_localizable_list, project):
    p_dict = defaultdict(int)

    #"""bugReport / summary / description / open / updated / reporterDN / reporterEmail / hasAttachment / attachmentTime / hasPR / commentsCount / project / bid / committerEmail / sameEmail / type / dev or user"""
    cocabu_path = '/home/ubuntu/Desktop/CoCaBu/'
    pickle_base = '/extdsk/iFixR/data/pickles/'
    issue_pickle_path = pickle_base + 'ALLbugReportsComplete_new.pickle'
    target_cnt = 0
    every_cnt = 0
    print('**' * 20 + project + '**' * 20)
    if (isfile(join(issue_pickle_path))):
        df = load_zipped_pickle(join(issue_pickle_path))
        for idx, bid in enumerate(df.bid.values):
            every_cnt += 1
            bid = df.iloc[idx]['bid']
            summary = df.iloc[idx]['summary']
            description = df.iloc[idx]['description']
            # project_ = df.iloc[idx]['project']
            dev_user = df.iloc[idx]['isDeveloper']
            reporter_email = df.iloc[idx]['reporterEmail']
            resolved = int(df.iloc[idx]['resolved'].split('-')[0])
            open_year = int(df.iloc[idx]['created'].split('-')[0])  # 2013
            open_date = str(df.iloc[idx]['created'].split('T')[0])  # 2013-09-07
            open_date_ = time.strptime(open_date, "%Y-%m-%d")
            if not bid in total_whole_list:
                continue
            p_dict[open_year] += 1
    print(p_dict)

if __name__ == "__main__":
    project_list = ['hive', 'hbase', 'camel', 'commons-lang', 'commons-math', 'commons-codec', 'commons-collections',
                    'commons-compress', 'commons-configuration', 'commons-io', 'spring-batch', 'spring-amqp']
    for idx, project in enumerate(project_list):
        trainTest(total_whole_list[idx], total_localizable_list[idx], project)
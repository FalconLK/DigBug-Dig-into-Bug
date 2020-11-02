import os, codecs, sys, gzip
sys.path.append('.')
sys.path.append('..')
from os.path import isfile, join, isdir
import pickle as p

# import lightgbm as light
# from commons import *
# from Preprocessor import preProcessing
from GitSearch.MyUtils import mkdir_p, cleanMetaPath, read_file, write_file_a

def processHunkData(target, output_path):
    print('\nProcessing hunk data...')
    """file / hunk / commitLog / repo / bid / commit / """
    commit_info = '/extdsk/iFixR/data/pickles/commits.pickle'
    valid_bid_set = set()
    normal_count = 0  # 393006
    java_count = 0  # 263083
    if (os.path.isfile(join(commit_info))):
        df = load_zipped_pickle(join(commit_info))
        for idx, file in enumerate(df.file.values):
            # print('Processing commit hunk side: %s/393006' % (normal_count))
            normal_count += 1
            if not file.split('/')[-1].endswith('.java'):
                continue

            # if file.split('/')[-1] == 'UDFToFloat.java':

            # print(file)
            # java_count += 1
            bid = df.iloc[idx]['bid']
            repo = df.iloc[idx]['repo']
            if not repo == target.lower():
                continue
            commit_hash = df.iloc[idx]['commit']
            commit_log = df.iloc[idx]['commitLog']
            hunk = df.iloc[idx]['hunk']

            final_path = output_path + 'hunks/' + str(repo).upper() + '/' + str(bid) + '/'
            if not os.path.isdir(final_path):
                mkdir_p(final_path)
            final_file = final_path + str(file).split('/')[-1]

            token_set = set()
            tokens = preProcessing(hunk)
            for token in tokens.split():
                token_set.add(token)
            token_str = ' '.join(token_set)

            write_file_a(final_file, token_str)

            valid_bid_set.add(bid)

            # else:
            #     continue

    print(normal_count)
    print(java_count)
    for bid in valid_bid_set:
        write_file_a(output_path + 'hunk_available_unique_bids.txt', str(bid))

    return valid_bid_set

def processReportData(output_path, valid_bid_set, period_limit):
    print('\nProcessing report data...')
    """bugReport / summary / description / created / updated / reporterDN / reporterEmail / hasAttachment / attachmentTime / hasPR / commentsCount / project / bid / committerEmail / sameEmail / type"""
    bug_info = '/extdsk/iFixR/data/pickles/ALLbugReportsComplete_new.pickle'
    normal_count = 0
    if (os.path.isfile(join(bug_info))):
        df = load_zipped_pickle(join(bug_info))
        for idx, bid in enumerate(df.bid.values):
            normal_count += 1
            print('Processing bug report side: %s/67868' % (normal_count))
            bid = df.iloc[idx]['bid']
            repo = df.iloc[idx]['project']  # repo
            type = df.iloc[idx]['type']  # bug ? none bug?
            summary = df.iloc[idx]['summary']
            description = df.iloc[idx]['description']
            # resolved = int(df.iloc[idx]['resolved'].split('-')[0])
            created = int(df.iloc[idx]['created'].split('-')[0])

            if created > period_limit:
                continue

            if not bid in valid_bid_set:
                continue

            if type == 'Bug':
                write_file_a(output_path + 'bug_only_ids.txt', bid)

            if summary == '' or summary is None: summary = ''
            if description == '' or description is None: description= ''

            final_path = output_path + 'reports/' + str(repo) + '/' + str(created) + '/'
            if not os.path.isdir(final_path):
                mkdir_p(final_path)
            final_file = final_path + str(bid) + '.txt'

            token_set = set()
            tokens = preProcessing(summary + ' ' + description)
            for token in tokens.split():
                token_set.add(token)
            token_str = ' '.join(token_set)

            write_file_a(final_file, token_str)

    print(normal_count)

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        return loaded_object

def getBugRatePerProject(target_project, period):
    """bugReport / summary / description / created / updated / reporterDN / reporterEmail / hasAttachment / attachmentTime / hasPR / commentsCount / project / bid / committerEmail / sameEmail / type"""
    bug_info = '/extdsk/iFixR/data/pickles/ALLbugReportsComplete_new.pickle'

    normal_count = 0
    report_cnt = 0
    bug_cnt = 0
    non_bug_cnt = 0

    if (os.path.isfile(join(bug_info))):
        df = load_zipped_pickle(join(bug_info))
        for idx, bid in enumerate(df.bid.values):
            normal_count += 1
            # print('Processing bug report side: %s/67868' % (normal_count))
            bid = df.iloc[idx]['bid']
            repo = df.iloc[idx]['project']  # repo
            type = df.iloc[idx]['type']  # bug ? none bug?
            summary = df.iloc[idx]['summary']
            description = df.iloc[idx]['description']
            resolved = int(df.iloc[idx]['resolved'].split('-')[0])
            created = int(df.iloc[idx]['created'].split('-')[0])

            if not repo == target_project:
                continue

            if created > int(period):
                continue

            # if not bid in unique_valid_bids:
            #     continue

            report_cnt += 1

            if type == 'Bug':
                write_file_a('bug_only_bids.txt', bid)
                bug_cnt += 1
            else:
                non_bug_cnt += 1

    print('Project: ', target_project)
    if report_cnt == 0:
        return

    rate = float(bug_cnt) / float(report_cnt)

    print('Project: ', target_project)
    print('# of Reports: ', report_cnt)
    print('# of Bugs: ', bug_cnt)
    print('# of Non-bugs: ', non_bug_cnt)
    print('Bug rate: ', rate)
    print('='*100)

    str_ = 'Project: ' + target_project + '\n' + \
        '# of Reports: ' + str(report_cnt)  + '\n' + \
        '# of Bugs: ' + str(bug_cnt) + '\n' + \
        '# of Non-bugs: ' + str(non_bug_cnt) + '\n' + \
        'Bug rate: ' + str(rate) + '\n' + \
        '=' * 100 + '\n'
    # write_file_a('bug_among_projects.txt', str_)

def findRoundabout(target, target_hunk_path, target_report_path, bug_only_bids, bug_only=False):
    hunk_bid_cnt = 0
    ''' Build Hunk - Token Dict '''
    bid_hunk_keyword_dict = dict()
    for bid in os.listdir(target_hunk_path):
        bid_path = target_hunk_path + bid
        hunk_bid_cnt += 1
        token_list = list()
        for file in os.listdir(bid_path):
            bid_file_path = bid_path + '/'+ file
            for token in read_file(bid_file_path).split():
                token_list.append(token)

        bid_hunk_keyword_dict[bid] = list(set(token_list))
    print('Hunk bid cnt: ', hunk_bid_cnt)

    report_bid_cnt = 0
    target_bid_cnt = 0

    ''' Compare with the report side '''
    for year in os.listdir(target_report_path):
        year_path = target_report_path + year

        for bid_file in os.listdir(year_path):
            report_bid_cnt += 1
            bid = bid_file.split('.')[0]
            if bug_only is True:            # Bug only 가 True면, bug 만 계산.
                if not bid in bug_only_bids:
                    continue

            bid_file_path = year_path + '/' + bid_file
            report_tokens = read_file(bid_file_path).split()
            # for token in read_file(bid_file_path).split():
            ''' Check if the token is in the hunk_keyword_dict (if it exists, there is intersection between the report and the hunk)'''
            for hunk_bid, hunk_tokens in bid_hunk_keyword_dict.items():
                if hunk_bid == bid:
                    if list(set(report_tokens) & set(hunk_tokens)):   # 여기가 True 면 intersection 존재
                        write_file_a('intersection_report_hunk.txt', bid + '$$' + str(list(set(report_tokens) & set(hunk_tokens))))
                    else:
                        write_file_a('intersection_X.txt', bid)
                        target_bid_cnt += 1
                # print (hunk_bid, token_lst)
    print('Report bid cnt: ', report_bid_cnt)
    print('bid with no intersection: ', target_bid_cnt)

if __name__ == '__main__':
    base_path = '/extdsk/icse_bug_loc/data/'
    period_limit_lst = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

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

    target_list = ['Apache/Hbase']
    period = '2019'

    for target in target_list:
        target = target.split('/')[1].upper()
        getBugRatePerProject(target, period)

    # bug_only_bids = read_file('bug_only_bids.txt').strip().split()
    # for target in target_list:
    #     target = target.split('/')[1].upper()
    #     target_hunk_path = hunk_path + target + '/'
    #     target_report_path = report_path + target + '/'
    #     findRoundabout(target, target_hunk_path, target_report_path, bug_only_bids, bug_only=False)
from DigBug.utils import load_zipped_pickle
from os.path import join, isfile
import sys, glob, os, xml, codecs
from bs4 import BeautifulSoup as Soup
import pickle

pickle_base = '/extdsk/iFixR/data/pickles/'
issue_pickle_path = pickle_base + 'ALLbugReportsComplete_new.pickle'
reporter_list = set()
developer_list = set()
if (isfile(join(issue_pickle_path))):
    df = load_zipped_pickle(join(issue_pickle_path))
    for idx, bid in enumerate(df.bid.values):
        bid = df.iloc[idx]['bid']
        reporter = df.iloc[idx]['reporterDN']
        dev_user = df.iloc[idx]['isDeveloper']
        reporter_list.add(reporter)
        if dev_user == True:
            developer_list.add(reporter)

Bench4BL = ['Apache/CAMEL', 'Apache/HBASE', 'Apache/HIVE', 'Commons/CODEC', 'Commons/COMPRESS', 'Commons/CRYPTO', 'Commons/IO', 'Commons/MATH', 'Commons/LANG', 'Commons/COLLECTIONS', 'Commons/CONFIGURATION', 'Commons/CSV', 'Commons/WEAVER', 'JBoss/ENTESB', 'JBoss/JBMETA', 'Spring/AMQP', 'Spring/DATAGRAPH', 'Spring/LDAP', 'Spring/SGF', 'Spring/SOCIALLI', 'Spring/ANDROID', 'Spring/DATAJPA', 'Spring/MOBILE', 'Spring/SHDP', 'Spring/SOCIALTW', 'Spring/BATCH', 'Spring/BATCHADM', 'Spring/DATACMNS', 'Spring/DATAMONGO', 'Spring/DATAREDIS', 'Spring/DATAREST', 'Spring/ROO', 'Spring/SEC', 'Spring/SECOAUTH', 'Spring/SHL', 'Spring/SPR', 'Spring/SOCIAL', 'Spring/SOCIALFB', 'Spring/SWF', 'Spring/SWS', 'Wildfly/ELY', 'Wildfly/SWARM', 'Wildfly/WFARQ', 'Wildfly/WFCORE', 'Wildfly/WFLY', 'Wildfly/WFMP']
bug_list = list()
bug_isDeveloper_dict = dict()
for project in Bench4BL:
    base = '/extdsk/Bench4BL/data/%s/bugrepo/bugs/' % project
    for xml_file in os.listdir(base):
        handler = open(base + xml_file).read()
        soup = Soup(handler, features='lxml')
        for item in soup.findAll('item'):
            title = str(item.find('title'))
            reporter = str(item.find('reporter').string)
            bug = title.split('[')[1].split(']')[0]
            bug_list.append(bug)
            if reporter in developer_list:
                print(True)
                bug_isDeveloper_dict[bug] = True
            else:
                bug_isDeveloper_dict[bug] = False

with open('bench_bug_dev_user.pickle', 'wb') as f:
    pickle.dump(bug_isDeveloper_dict, f)

with open("bench_bug_dev_user.pickle", "rb") as f:
    load = pickle.load(f)


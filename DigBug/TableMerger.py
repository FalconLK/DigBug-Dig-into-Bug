import os, csv
from GitSearch.MyUtils import mkdir_p, write_file_a, read_file
current_path = os.path.dirname(os.path.abspath(__file__)) + '/'

def mergeTables():
    project_list = ['spring-data-redis', 'wildfly', 'commons-collections', 'wildfly-arquillian', 'spring-amqp',
                    'wildfly-swarm',
                    'spring-data-rest', 'spring-social-linkedin', 'spring-mobile', 'commons-codec', 'commons-compress',
                    'spring-data-jpa', 'spring-social-twitter', 'spring-ldap', 'commons-crypto',
                    'spring-security-oauth', 'spring-batch', 'hbase', 'commons-csv', 'spring-data-mongodb',
                    'spring-data-commons', 'spring-android', 'commons-io', 'spring-social', 'wildfly-maven-plugin',
                    'spring-security', 'wildfly-elytron', 'hive', 'spring-social-facebook', 'commons-configuration',
                    'camel', 'spring-roo', 'wildfly-core', 'spring-batch-admin'
                    ]

    cnt = 0
    line_list = list()
    for project in project_list:
        cont = read_file(current_path + 'decision_tables/decision_table_%s.csv' % project)
        for idx, line in enumerate(cont.split('\r\n')):
            if cnt == 0 and idx == 0:
                header = line
                line_list.append(header)
            cnt += 1
            if idx == 0:
                continue

            line_list.append(line)

    merged_path = current_path + 'decision_tables/merged_table.csv'
    if os.path.isfile(merged_path):
        os.remove(merged_path)

    line_cnt = 0
    for line in line_list:
        line_cnt += 1
        write_file_a(merged_path, line)

    print("Total number of targets: ", line_cnt)




mergeTables()
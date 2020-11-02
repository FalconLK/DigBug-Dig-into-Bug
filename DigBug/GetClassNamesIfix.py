import os
from GitSearch.MyUtils import md5, so_tokenizer, copytree, mkdir_p, cleanMetaPath, write_file_a, read_file

def takeJavaFiles(directory):
    javafiles = (os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(directory)
        for f in files if f.endswith('.java'))
    return javafiles

def getClassNames(src, dst_file):
    global tmp_set
    javafiles = takeJavaFiles(src)  # 자바 파일들만 뽑아내는 함수
    i = 0

    for javafile in javafiles:
        i += 1
        if i % 1000 == 0:  # 1000개 될때마다 프린트 한번씩
            print("Counter: %s" % i)
            # print "typed_method_call" + str(counter.typed_method_call_count)
        class_name = javafile.split('/')[-1]
        write_file_a(dst_file, class_name)


''' D & C '''
current_path = os.path.dirname(os.path.abspath(__file__)) + '/'
git_repo_path = '/extdsk/iFixR/data/gitrepo_old/'
for dir in os.listdir(git_repo_path):  # 모든 디렉토리 밑 파일들
    print('Processing project: ', dir)
    class_file = current_path + 'classes_%s.txt' % dir
    if os.path.isfile(class_file):
        os.remove(class_file)
    getClassNames(git_repo_path + dir, class_file)


# ''' Bench4BL '''
# target_list = ['Commons/Math', 'Apache/Hive', 'Apache/Hbase', 'Apache/Camel',
#                    'Commons/Codec', 'Commons/Collections', 'Commons/Compress', 'Commons/Configuration',
#                    'Commons/Crypto',
#                    'Commons/Csv', 'Commons/Io', 'Commons/Lang', 'Commons/Weaver',
#                    'JBoss/Entesb', 'JBoss/Jbmeta',
#                    'Previous/AspectJ', 'Previous/Jdt', 'Previous/Pde', 'Previous/Swt', 'Previous/Zxing',
#                    'Spring/Amqp', 'Spring/Batchadm', 'Spring/Datajpa', 'Spring/Datarest', 'Spring/Roo',
#                    'Spring/Sgf', 'Spring/Social', 'Spring/Socialtw', 'Spring/Sws', 'Spring/Android',
#                    'Spring/Datacmns', 'Spring/Datamongo', 'Spring/Ldap', 'Spring/Sec', 'Spring/Shdp',
#                    'Spring/Socialfb', 'Spring/Spr', 'Spring/Batch', 'Spring/Datagraph', 'Spring/Dataredis',
#                    'Spring/Mobile', 'Spring/Secoauth', 'Spring/Shl', 'Spring/Socialli', 'Spring/Swf',
#                    'Wildfly/Ely', 'Wildfly/Swarm', 'Wildfly/Wfarq', 'Wildfly/Wfcore', 'Wildfly/Wfly', 'Wildfly/Wfmp'
#                    ]  ## 'Previous/AspectJ', 'Previous/Jdt', 'Previous/Pde', 'Previous/Swt', 'Previous/Zxing'
#
# base = '/extdsk/Bench4BL/data/'
# for target in target_list:
#     lst = takeJavaFiles(base + target.split('/')[0] + '/' + target.split('/')[1].upper() + '/gitrepo/')
#     for c in lst:
#         write_file_a('class_names_per_project/classes_%s.txt' % target.split('/')[-1], c)
from GitSearch.MyUtils import read_file
import os

dir = '/extdsk/Defects4J/commons-lang/src/main'

def java_files_from_dir(directory):
    javafiles = (os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(directory)
        for f in files if f.endswith('.java'))
    return javafiles

cnt = 0
for i in java_files_from_dir(dir):
    cnt += 1
print (cnt)

    # if i == '/extdsk/Defects4J/commons-lang/src/main/java/org/apache/commons/lang3/text/translate/EntityArrays.java':
    #     continue
    # os.remove(i)


# answer_cnt = 0
# file_cnt = 0
# for i in os.listdir(dir):
#     answer_cnt += 1
#     file_cnt += len(read_file(dir + '/' + i).splitlines())
#
# print ('\nAnswer bug report count: ', answer_cnt)
# print ('Total related file count: ', file_cnt)
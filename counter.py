#-*- coding: utf-8 -*-
from utils import mkdir_p, write_file_a, read_file, cleanMetaPath, load_zipped_pickle
from collections import defaultdict
import sys, os
sys.path.append('.')
sys.path.append('..')
rootdir = 'path'

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
bucket_report_cnt = defaultdict(int)
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        contents = read_file(os.path.join(subdir, file))
        num_lines = file_len(os.path.join(subdir, file))
        bucket_report_cnt[file.split('.')[0]] += num_lines
from collections import OrderedDict
ordered_dictionary = OrderedDict(sorted(bucket_report_cnt.items(), key=lambda item: int(item[0])))
for i,v in ordered_dictionary.items():
    print(i, v)

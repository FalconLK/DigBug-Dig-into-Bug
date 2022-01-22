#-*- coding: utf-8 -*-
from os.path import join
import pickle
import gzip, logging, sys, os, csv, time
sys.path.append('.')
sys.path.append('..')
from utils import mkdir_p, write_file_a, read_file, cleanMetaPath
from os.path import join, isfile
import sys, glob, os, xml, codecs
from bs4 import BeautifulSoup as Soup
from shutil import copyfile
if __name__ == "__main__":
    original_source = 'path'
    info_zilla_result = 'path'
    dest_path = 'path'
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
    for project in os.listdir(info_zilla_result):
        project_path = dest_path + project
        if not os.path.isdir(project_path):
            os.mkdir(project_path)
        for bucket in os.listdir(info_zilla_result + project):
            project_bucket_path = project_path + '/' + bucket.split('.')[0]
            if not os.path.isdir(project_bucket_path):
                os.mkdir(project_bucket_path)
            file_cont = read_file(info_zilla_result + project + '/' + bucket)
            print(file_cont)
            for bug in file_cont.split('\n'):
                original_file = original_source + project + '/' + bug + '.txt'
                dest_file = project_bucket_path + '/' + bug + '.txt'
                if bug == '' or os.path.isfile(dest_file):
                    continue
                if not bug.split('-')[0].upper() == project.upper():
                    continue
                copyfile(original_file, dest_file)

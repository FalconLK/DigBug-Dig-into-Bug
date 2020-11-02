#-*- coding: utf-8 -*-
# from __future__ import print_function
from bs4 import BeautifulSoup
from GitSearch.MyUtils import read_file, write_file, mkdir_p, cleanMetaPath
import cgi, codecs, os, time, re, urllib2, urllib, csv

def localize_floats(row):
    return [
        str(el).replace('.', ',') if isinstance(el, float) else el
        for el in row
    ]

if __name__ == "__main__":
    base_path = '/home/ubuntu/Desktop/CoCaBu/'
    answer_path = base_path + 'answer_bench4bl/'

    # Augmentation
    # result_file = base_path + '/results.csv'
    # recommended_path = base_path + 'recommended/'

    # NO Augmentation
    recommended_path = base_path + 'test_augment_3_full/'
    result_file = base_path + 'new_results_both_augment_3_full.csv'

    group = 'Apache'
    project = ''
    bug_id = ''
    version = 'all'
    answer_file_cnt = ''

    if os.path.isfile(result_file):
        os.remove(result_file)
    results_fp = open(result_file, 'tmp')
    results_writer = csv.writer(results_fp)

    for path, dirs, files in os.walk(recommended_path):
        c = 1
        for dir in dirs:
            sub_dir = os.path.join(path, dir)
            file_list = os.listdir(sub_dir)
            for file in file_list:
                recommended_file = os.path.join(sub_dir, file)
                results = read_file(recommended_file)
                project = recommended_file.split('/')[6].split('_')[0]
                bug_id = recommended_file.split('/')[-1].split('.')[0]
                source_version = recommended_file.split('/')[-2]

                # corresponding answer file check
                answer_file = answer_path + '/'.join(recommended_file.split('/')[6:])
                if not os.path.isfile(answer_file):
                    continue
                answers = read_file(answer_file)
                answer_list = list()
                for answer in str(answers).split('\n'):
                    if not answer == '':
                        answer_list.append(answer)
                answer_file_cnt = len(answer_list)

                # write the csv
                answer_order = 0
                precision_sum = 0
                input = list()
                flag = 0

                tmp = []
                file_found_cnt = 0
                for idx, result in enumerate(str(results).split('\n')):
                    if result == '' or not result in answer_list or result in tmp:
                        continue

                    file_found_cnt += 1
                    #dup check
                    tmp.append(result)

                    flag = 1
                    answer_order += 1

                    rank = idx + 1
                    if rank == 1:
                        top1 = 1
                        top5 = 1
                        top10 = 1
                    elif rank <= 5:
                        top1 = 0
                        top5 = 1
                        top10 = 1
                    elif rank <= 10:
                        top1 = 0
                        top5 = 0
                        top10 = 1
                    else:
                        top1 = 0
                        top5 = 0
                        top10 = 0

                    p_rank = float(answer_order) / float(rank)
                    precision_sum += p_rank

                    # localize_floats(row)
                    input.append(localize_floats([group, project, source_version, bug_id, version, answer_file_cnt, result, str(top1), str(top5), str(top10), str(rank), answer_order, p_rank]))

                if flag == 0:
                    for i in answer_list:
                        input.append([group, project, source_version, bug_id, version, answer_file_cnt, 'None', '0', '0', '0', '0', '0', '0'])

                if answer_order == 0:
                    ap = 0
                else:
                    ap = float(precision_sum) / float(file_found_cnt)
                print 'precision_sum:', precision_sum, 'answer_order: ', answer_order, 'ap: ', ap

                for i in input:
                    i.append(ap)
                    i.append(str(file_found_cnt))
                    results_writer.writerow(localize_floats(i))
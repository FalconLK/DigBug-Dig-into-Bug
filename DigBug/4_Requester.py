#-*- coding: utf-8 -*-

''' Input from Defects4J '''
''' Getting results as well '''

from bs4 import BeautifulSoup
import pickle as p
import gzip, logging, sys, time, os, requests, re
sys.path.append('.')
sys.path.append('..')
from subprocess import Popen, PIPE
from subprocess import CalledProcessError
import cgi, codecs, os, time, re, urllib, csv
from similarity.cosine import Cosine

from Preprocessor import preBasic, SPC, CMC, STM, SWR, mathProcessing, getTokens, postBasic

cocabu_path = os.path.dirname(os.path.abspath(__file__)) + '/'

def specialCharTokenizer(text):
    special_char_list = ['|', '=', '/', '(', ')', '[', ']', ',', '.', '_', '\'', '`', '!', '@', '#', '$', '%', '^', '&',
                         '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"', '\\']
    for s_char in special_char_list:
        text = text.replace(s_char, ' ')
    return text

def read_file(file_path):
    try:
        with codecs.open(file_path, mode='r', encoding=u'utf-8') as file:
            text = file.read()
        file.close()
    except:
        return None
    return text

def write_file(file_path, content):
    try:
        with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
            file.write(content + "\n")
    except:
        return None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if os.path.isdir(path):
            pass
        else:
            raise


def cleanMetaPath(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def localize_floats(row):
    return [
        str(el).replace('.', ',') if isinstance(el, float) else el
        for el in row
    ]

def java_files_from_dir(directory):
    java_file_list = list()
    for dirpath, dirnames, files, in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                java_file_list.append(file)
    return java_file_list

def setLogg():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        return loaded_object

def shellGitCheckout(cmd,enc='utf-8'):
    try:
        with Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True,encoding=enc) as p:
            output, errors = p.communicate()
            # print(output)
            if errors:
                raise CalledProcessError(errors, '-1')
            output
    except CalledProcessError as e:
        logging.warning(errors)

    return output,errors

def write_file_a(file_path, content):
    with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
        file.write(content + "\n")

def write_file_w(file_path, content):
    with codecs.open(file_path, mode='w', encoding='utf-8') as file:
        file.write(content + "\n")

class RecommendExperiment(object):
    content_type = u'utf-8'
    base_url = u''
    src_path = u''
    dest_path = u''
    fail_path = u''

    def __init__(self, src, dst, base_url, fail_path, target):
        self.src_path = src
        self.dest_path = dst
        self.base_url = base_url
        self.fail_path = fail_path
        self.target = target

    def get_body_POST(self, param):
        param = cgi.escape(re.sub(r'[^\x00-\x80]+', '', param))

        ###### Part for POST method by 'requests'
        # param = urllib.quote(param).encode(u'utf-8')
        param = {"key": param}

        # print ('*******: ', param)
        try:
            # r = requests.post("http://code-search.uni.lu/cocabu", data=param)
            r = requests.post(self.base_url, data=param)
            # print (r.status_code, r.reason)
        except Exception as e:
            write_file_a(self.fail_path, param.split('$$')[0])
            print (e)

        ###### Part for POST method by 'urllib2.Request' [Not working so far]
        # param = urllib.quote(param).encode(u'utf-8')
        # request = urllib2.Request((self.base_url + u'/?q=').encode(u'utf-8'))
        # param = {"key": param}
        # json_param = json.dumps(param)
        # request.add_data(json_param)
        # if self.content_type == u'utf-8':  # if is_utf8 is True:
        #     request.add_header(u'content-type', u'charset=utf-8')
        # request.add_header(u'User-Agent', u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')

        # request.add_header(u'User-agent', u'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')
        # request.add_header(u'User-Agent', u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        # u'Accept', u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # u'Accept-Charset', u'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # u'Accept-Encoding', u'none',
        # u'Accept-Language', u'en-US,en;q=0.8',
        # u'Connection', u'keep-alive')


    def get_body_GET(self, param):
        param = cgi.escape(re.sub(r'[^\x00-\x80]+', '', param))
        ##### Original part for GET method
        request_url = self.base_url + u'/?q=' + urllib.quote(param)
        request = urllib2.Request(request_url.encode(u'utf-8'))  # create request object   # Advanced request

        if self.content_type == u'utf-8':  # if is_utf8 is True:
            request.add_header(u'content-type', u'charset=utf-8')
        request.add_header(u'User-Agent', u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
        # request.add_header(u'User-agent', u'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')
        # request.add_header(u'User-Agent', u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        # u'Accept', u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # u'Accept-Charset', u'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # u'Accept-Encoding', u'none',
        # u'Accept-Language', u'en-US,en;q=0.8',
        # u'Connection', u'keep-alive')
        try:
            response = urllib2.urlopen(request)
            resText = response.read()
        except Exception as e:
            write_file_a(self.fail_path, param.split('$$')[0])
            print (e)

    def run(self, feature_flag, pp_option):
        print(u"Start running...\n")
        # project_list = os.listdir(file_path)   #file_path = u"/Users/Falcon/Desktop/Kui/FacoyInput/"
        # print (project_list)

        # project_list = sorted(project_list)
        # # 이렇게하면 문자열 내의 숫자순으로 정렬 가능.
        # arr = [int(re.search(r"(\d+)", item).group(1)) for item in project_list]
        # a1 = zip(project_list, arr)
        # a1.sort(key=lambda item: item[1])
        # a2, a3 = zip(*a1)
        # #----------------------- a2 가 결과임.

        query_count = 0
        for bug_report in os.listdir(self.src_path):
            result_file = self.dest_path + bug_report
            print('****** %s' % self.src_path + bug_report)
            if not os.path.isfile(self.src_path + bug_report):
                continue

            file_content = read_file(self.src_path + bug_report).strip()   #Tokenized query 를 보내면 yandex 에서 검색할때 결과가 이상할 수 있음.

            if pp_option == 'preBasic':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                file_content = postBasic(tokens)

            elif pp_option == 'SPC':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                file_content = postBasic(tokens)

            elif pp_option == 'CMC':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SWR':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = SWR(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'STM':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = STM(tokens)
                file_content = postBasic(tokens)


            elif pp_option == 'SPC_CMC':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SPC_SWR':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = SWR(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SPC_STM':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = STM(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'CMC_SWR':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                tokens = SWR(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'CMC_STM':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                tokens = STM(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SWR_STM':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = SWR(tokens)
                tokens = STM(tokens)
                file_content = postBasic(tokens)


            elif pp_option == 'SPC_CMC_SWR':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                tokens = SWR(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SPC_CMC_STM':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                tokens = STM(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SPC_SWR_STM':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = SWR(tokens)
                tokens = STM(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'CMC_SWR_STM':
                file_content = preBasic(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                tokens = SWR(tokens)
                tokens = STM(tokens)
                file_content = postBasic(tokens)

            elif pp_option == 'SPC_CMC_SWR_STM':
                file_content = preBasic(file_content)
                file_content = SPC(file_content)
                tokens = getTokens(file_content)
                tokens = CMC(tokens)
                tokens = SWR(tokens)
                tokens = STM(tokens)
                file_content = postBasic(tokens)

            else:
                print('Please configure the preprocessing option!!!!!')
                time.sleep(100000)




            query = self.target + '$$' + result_file + '$$' + pp_option + '$$' + file_content
            if feature_flag == 1:
                self.get_body_POST(query)
            else:
                self.get_body_GET(query)
            query_count += 1
            # print ('==============================================================================%s / %s' % (query_count, bug_report.split('/')[-1]))
        return query_count

def check_feature(result_path):
    tmp = result_path.split('/')[-2].split('_')
    if 'description' in tmp:
        return 1
    else:
        return 0

def generateResults(target, result_path, project, existing_file_list, input_path, answer_path, pp_option, cn_option, bucket_number):
    recommended_path = result_path + '%s_details/%s/%s/%s/' % (project, bucket_number, pp_option, cn_option)

    final_path = result_path + '%s/' % project
    if not os.path.isdir(final_path):
        mkdir_p(final_path)

    result_file = final_path + '%s_%s_%s_%s.csv' % (project, bucket_number, pp_option, cn_option)


    group = 'Apache'
    version = 'all'

    if os.path.isfile(result_file):
        os.remove(result_file)
    results_fp = open(result_file, 'tmp')
    results_writer = csv.writer(results_fp)

    # 결과 나온 것들에 대해서만 계산
    unique_bug = set()
    for path, dirs, files in os.walk(recommended_path):  # 디렉토리 밑 모든 파일들
        for file in files:
            csv_input_line = list()
            results = read_file(path + file)
            result_list = results.split('\n')
            bug_id = file.split('/')[-1].split('.')[0]
            unique_bug.add(bug_id)

            ''' List corresponding answer files '''
            answer_file = answer_path + file
            if not os.path.isfile(answer_file):
                continue
            answers = read_file(answer_file)
            answer_list = list()
            for answer in str(answers).split('\n'):
                if not answer == '':
                    answer_list.append(answer)
            answer_file_cnt = len(answer_list)

            ''' Check if there is the target file in the current project '''
            # 개발자 입장에서는 현존하지 않는 module 을 고칠 순 없으니 제외해야 맞다.
            # 다른 의견, 프로젝트들 마다 항상 최신 버전을 사용하는 사람들만 존재할 수 없고, 각기 다른 버전을 사용하는 사람이 올리는 버그리포트 일수도 있다. 따라서 다른 놈들은 제외하지 않고 그대로 얻어 맞았다.
            # existOrNot = 0
            # for answer in answer_list:
            #     if answer in existing_file_list:
            #         existOrNot = 1
            # if existOrNot == 0:
            #     continue

            query_title = read_file(input_path + file).split('\n')[0]
            flag = 0

            '''if candidate is from the title itself (exactly matched with the title [ex. MathUtils.toMulti]), give it the priority'''
            candidate = ''

            '''title priority parsing every token'''
            # 아래 방법들은 전부 CamelCase 그대로 두고, Stemming 도 하면 안된다. 토큰은 ['.', '(', ')', '?', ] 와 같은 special character 로 tokenize 하면 됨.
            # LANG-368 의 경우 Title 이 (FastDateFormat getDateInstance() and getDateTimeInstance() assume Locale.getDefault() won't change)
            # 이런 경우, Project's current version file list 가지고 있다가 각 토큰 하나하나와 비교 한다음, 맞는게 있으면 그걸 가져와서 1위 랭크에 놓으면 되겠다.
            # LANG-636 의 경우 Title 이 (text.ExtendedMessageFormat doesn't override java.text.MessageFormat.equals(Object))
            # 이런 경우, Project's current version file list 내부에 2개 (ExtenedMessageFormat, MessageFormat)가 존재할 수 있다. 그러면??? 왠만하면 첫번째꺼 선택



            '''title priority using regex'''
            # query_title_tokens = query_title.split(' ')
            # for token in query_title_tokens:
            #     if re.search('\.[A-Za-z]', token):
            #         candidate = token.split('.')[0] + '.java'
            #         break   # 여기서 break 를 걸면, 첫번째 candidate 만을 취급하게 된다. 이것도 결과에 영향을 끼치는구나..


            # 위의 방법들 로도 못찾는 것들은 각 파일들 이름과 title 의 similarity (cosine) 비교를 해보면 되지 않을까?

            if cn_option == 'ON':
                query_title = specialCharTokenizer(query_title)
                query_title_tokens = query_title.split(' ')
                for token in query_title_tokens:  # Title 의 각 토큰들 전부 하나하나 대조 시작
                    token_java = token + '.java'
                    if token_java in existing_file_list:
                        candidate = token_java
                        break
                if candidate:                                                                           # answer list 에 포함되는지 여기서 확인 해야만 하는 이유는 candidate 이 있다 해서 무조건 맞는게 아니기 때문.
                    result_list.insert(0, candidate)
                    if candidate in answer_list:
                        write_file_a('success_candidates.txt', bug_id + ' : ' + candidate)
                        # csv_input_line.append(localize_floats([group, target, 'tmp', bug_id, version, answer_file_cnt, candidate, 1, 1, 1, 1, 1, 1, 1, ' ', candidate]))
                        # print(bug_id, 'rank: ', str(1), 'precision_sum: ', 1, 'answer_order: ', 1, 'ap: ', 1, '*')
                        # for i in csv_input_line:
                        #     results_writer.writerow(localize_floats(i))
                        # continue
                    else:                                                                               # Candidate 이 있는데 틀릴 경우, 어쨋든 결과에 안좋게 반영하는게 맞다. 우리는 answer를 모르는 상태이기 때문 .
                        write_file_a('false_candidates.txt', bug_id + ' : ' + candidate)

            answer_order = 0
            precision_sum = 0
            tmp = []
            file_found_cnt = 0
            rank = 0
            for idx, result in enumerate(result_list):
                if result == '' or not result in answer_list or result in tmp:  # 여기서 answer list 안에 없는지 체크해도 되는 이유는 idx 사용.
                    continue
                file_found_cnt += 1

                ''' Duplicate checking '''
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

                if answer_order == 1:
                    mr = p_rank
                else:
                    mr = ''

                # localize_floats(row)
                csv_input_line.append(localize_floats([group, target, '', bug_id, version, answer_file_cnt, result, str(top1), str(top5), str(top10), str(rank), answer_order, p_rank, mr]))

            if flag == 0:  # 전부 실패시.
                for i in answer_list:
                    csv_input_line.append([group, target, '', bug_id, version, answer_file_cnt, 'None', '0', '0', '0', '0', '0', '0', '0'])
                    break

            if answer_order == 0 or answer_file_cnt == 0:
                ap = 0
            else:
                # ap = float(precision_sum) / float(file_found_cnt)  #answer_file_cnt 로 나누면 낮아짐.
                ap = float(precision_sum) / float(answer_file_cnt)  # answer_file_cnt 로 나누면 낮아짐.




            ''' 결과보정: get the similarity between recommended files and the title and take the top 1 '''
            # if ap < 0.2:
            #     result_dict = dict()
            #     cosine = Cosine(2)
            #     for result in read_file(recommended_path + file).splitlines():
            #         str_1 = query_title
            #         str_2 = result
            #         p0 = cosine.get_profile(str_1)
            #         p1 = cosine.get_profile(str_2)
            #         result_dict[result] = cosine.similarity_profiles(p0, p1)
            #         # print(cosine.similarity_profiles(p0, p1))
            #
            #     sorted_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
            #     trick = sorted_dict[0][0]
            #     if trick in answer_list:
            #         # csv_input_line.insert(0, localize_floats([group, target, '', bug_id, version, answer_file_cnt, result, str(top1), str(top5), str(top10), str(rank), answer_order, p_rank]))
            #         csv_input_line[0] = localize_floats([group, target, 'aa', bug_id, version, str(answer_file_cnt), trick, str(1), str(1), str(1), str(1), str(1), str(1), str(1), '', candidate])
            #         print(bug_id, 'rank: ', str(1), 'precision_sum: ', 1, 'answer_order: ', 1, 'ap: ', 1, '**')
            #         for i in csv_input_line:
            #             results_writer.writerow(localize_floats(i))
            #         continue

            print(bug_id, 'rank: ', str(rank), 'precision_sum: ', precision_sum, 'answer_order: ', answer_order, 'ap: ', ap)

            for idx, i in enumerate(csv_input_line):
                if idx == 0:
                    i.append(ap)
                    i.append(candidate)
                else:
                    i.append('')

                # i.append(str(file_found_cnt))
                results_writer.writerow(localize_floats(i))



# 아래 리스트 자동화 시켜야 함.
    """
    1_def4j_math_SO1_rep_init
    2_def4j_math_SO1_rep_q_desc
    3_def4j_math_SO1_rep_a_desc
    4_def4j_math_SO1_rep_a_snip
    5_def4j_math_SO1_com_init_q_desc
    6_def4j_math_SO1_com_init_a_desc
    7_def4j_math_SO1_com_init_a_snip
    8_def4j_math_SO1_com_q_desc_a_desc
    9_def4j_math_SO1_com_q_desc_a_snip
    10_def4j_math_SO1_com_a_desc_a_snip
    11_def4j_math_SO1_com_init_q_desc_a_desc
    12_def4j_math_SO1_com_init_q_desc_a_snip
    13_def4j_math_SO1_com_init_a_desc_a_snip
    14_def4j_math_SO1_com_q_desc_a_desc_a_snip
    15_def4j_math_SO1_com_init_q_desc_a_desc_a_snip
    16_def4j_math_SO1_rep_a_snip_pure
    17_def4j_math_SO1_rep_a_snip_pure_no_struct
    18_def4j_math_Bug1
    """

def clean(cocabu_path, fail_path, result_path):
    if os.path.isfile(fail_path):
        os.remove(fail_path)
    if os.path.isfile(cocabu_path + 'useBRorNot.txt'):
        os.remove(cocabu_path + 'useBRorNot.txt')
    if os.path.isfile(cocabu_path + 'useIRorNot.txt'):
        os.remove(cocabu_path + 'useIRorNot.txt')
    if os.path.isfile(cocabu_path + 'success_candidates.txt'):
        os.remove(cocabu_path + 'success_candidates.txt')
    if os.path.isfile(cocabu_path + 'false_candidates.txt'):
        os.remove(cocabu_path + 'false_candidates.txt')
    if os.path.isdir(result_path):
        cleanMetaPath(result_path)
    else:
        mkdir_p(result_path)

def inputAnswerValidater(input_path, answer_path):
    inputs = os.listdir(input_path)
    answers = os.listdir(answer_path)
    print(inputs)
    print()
    print(answers)


from shutil import copyfile
input_base = '/extdsk/bug_localization/input_answer/'
def generateInput(project, bucket_number, target_bucket_list):
    bucket_dir = input_base + 'input_decision/' + project + '/' + bucket_number
    original_input_path = input_base + 'input_bench4bl/%s/' % project.split('/')[-1].capitalize()
    if not os.path.isdir(bucket_dir):
        mkdir_p(bucket_dir)
    else:
        cleanMetaPath(bucket_dir)

    for file in os.listdir(original_input_path):
        bid = file.split('.')[0]
        if bid in target_bucket_list:
            input_file = original_input_path + bid + '.txt'
            copyfile(input_file, bucket_dir + '/%s.txt' % bid)

def generateAnswer(project, bucket_number, target_bucket_list):
    bucket_dir = input_base + 'answer_decision/' + project + '/' + bucket_number
    original_answer_path = input_base + 'answer_bench4bl/%s/' % project.split('/')[-1].capitalize()
    if not os.path.isdir(bucket_dir):
        mkdir_p(bucket_dir)
    else:
        cleanMetaPath(bucket_dir)
    for file in os.listdir(original_answer_path):
        bid = file.split('.')[0]
        if bid in target_bucket_list:
            answer_file = original_answer_path + bid + '.txt'
            copyfile(answer_file, bucket_dir + '/%s.txt' % bid)

def expBench4BLForAll():
    # base_url = u'http://code-search.uni.lu/cocabu'        # External request

    # now the 4568 is being used for the CoCaBu service
    base_url = u'http://localhost:4569'
    data_path = '/extdsk/bug_localization/'



    ''' Parameters '''
    ###################################################################################################################
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

    pp_option_list = ['preBasic',
                      'SPC', 'CMC', 'SWR', 'STM', 'SPC_CMC', 'SPC_SWR', 'SPC_STM', 'CMC_SWR', 'CMC_STM', 'SWR_STM',
                      'SPC_CMC_SWR', 'SPC_CMC_STM', 'SPC_SWR_STM', 'CMC_SWR_STM', 'SPC_CMC_SWR_STM']

    # ClassName effect options
    cn_option_list = ['OFF', 'ON']

    ###################################################################################################################
    '''Copy the original input to bucket input'''
    # for target in target_list:
    #     print(target)
    #     bucket_id_path = '/home/ubuntu/Desktop/CoCaBu/DigBug/buckets/%s' % target.split('/')[-1]
    #     for bucket in os.listdir(bucket_id_path):
    #         bucket_number = bucket.split('.')[0]
    #         print(bucket_number)
    #         target_bucket_list = list()
    #         contents = read_file(bucket_id_path + '/' + bucket)
    #         for bid in contents.splitlines():
    #             target_bucket_list.append(bid)
    #
    #         generateInput(target.split('/')[-1], bucket_number, target_bucket_list)
    #         generateAnswer(target.split('/')[-1], bucket_number, target_bucket_list)    # input answer 먼저 체크하고
    ###################################################################################################################

    input_decision_base = '/extdsk/bug_localization/input_answer/input_decision/'

    print ('\n\n\n\n\n************************************************************************************')
    for idx, target in enumerate(target_list):

        print("Current target: ", target)
        '''Bench4BL path'''
        project_path = u'/extdsk/Bench4BL/data/%s/gitrepo/' % (target.split('/')[0] + '/' + target.split('/')[1].upper())

        for bucket_number in os.listdir(input_decision_base + target.split('/')[-1]):

            print("Current bucket number: ", bucket_number)
            '''Bucket input path'''
            input_path = data_path + 'input_answer/input_decision/%s/' % target.split('/')[1] + bucket_number + '/'
            answer_path = data_path + 'input_answer/answer_decision/%s/' % target.split('/')[1] + bucket_number + '/'

            for idx, pp_option in enumerate(pp_option_list):
                print("Preprocessing option: ", pp_option)

                for idx, cn_option in enumerate(cn_option_list):
                    print("ClassName effect option: ", cn_option)
                    print('************************************************************************************')

                    '''Result path'''
                    project = str(target.split('/')[1].lower())  # hive
                    result_base_path = data_path + 'results_decision/'
                    result_path = result_base_path + u'%s_details/%s/%s/%s/' % (project, bucket_number, pp_option, cn_option)
                    fail_path = result_base_path + u'fail_' + u'%s_%s_%s_%s.txt' % (project, bucket_number, pp_option, cn_option)

                    feature_flag = True

                    clean(cocabu_path, fail_path, result_path)
                    exp = RecommendExperiment(input_path, result_path, base_url, fail_path, target)
                    query_count = exp.run(feature_flag, pp_option)
                    print('Final query count: ', query_count)

                    existing_file_list = java_files_from_dir(project_path)
                    generateResults(target, result_base_path, project, existing_file_list, input_path, answer_path, pp_option, cn_option, bucket_number)

                    # inputAnswerValidater(input_path, answer_path)

if __name__ == "__main__":





    expBench4BLForAll()

'''
[B] baseline
[SPC] split by special char
[CMC] split by camel case
[STM] stemming
[SWR] stop words removal 
'''


'''
[CNE] class name effect
[DEV] developer vs user 
'''
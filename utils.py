#-*- coding: utf-8 -*-
import gzip
import pickle as p
import os, codecs, shutil

stopwords = ['', 'secondly', 'all', 'gt', 'consider', 'pointing', 'whoever', 'global', 'felt', 'four', 'edu',
                 'go', 'mill', 'oldest', 'causes', 'seemed', ' ', 'certainly', 'const', 'doe', "when's",
                 'becausebecomebecomes', 'vs', 'young', 'presents', 'to', 'finally', 'asking', 'present', 'th',
                 'under', 'sorry', "tmp's", 'sent', 'insofar', 'far', 'void', 'every', 'yourselves',
                 'little', "we'll", 'presented', 'did', 'turns', 'list', "they've", 'beforehand', 'try', 'p',
                 'small', 'thereupon', "it'll", "i'll", 'parted', 'smaller', 'says', "you'd", 'ten', 'likely',
                 'further', 'even', 'what', 'sub', 'fact', 'while', 'above', 'sup', 'new', 'rd', 'ever', 'public',
                 'can', 'full', "c'mon", 'whose', 'respectively', 'sincere', 'never', 'here', 'youngest', 'let',
                 'groups', 'others', "hadn't", 'along', "aren't", 'fifteen', 'great', 'k', 'allows', 'amount',
                 "i'd", 'howbeit', "he'd", 'usually', 'que', "i'm", 'changes', 'thats', 'hither', 'via', 'followed',
                 'members', 'tr', 'merely', 'private', 'ask', 'viz', 'txt', 'everybody', 'use', 'from',
             'synchronized', 'working', 'contains', 'two', 'next', 'eleven', 'call', 'therefore', 'taken',
             'themselves', 'thru', 'until', 'today', 'more', 'throws', 'knows', 'mr', 'becomes', 'hereby',
             'herein', 'needed', 'downing', "ain't", 'particular', 'known', 'cases', 'must', 'me', 'high',
             'none', 'room', 'thanks', 'f', 'this', 'oh', 'anywhere', 'nine', 'thin', 'v', 'following',
             'making', 'my', 'example', 'numbers', 'overrid', 'indicated', 'give', "didn't", 'states',
             'indicates', 'something', 'want', 'bottombut', 'needs', 'end', 'turn', 'rather', 'six', 'off',
             'how', 'get', 'instead', 'itse', 'okay', 'tried', 'may', 'after', 'different', 'tries', 'such',
             'man', 'tmp', 'third', 'whenever', 'maybe', 'appreciate', 'so', 'q', 'switch', 'cannot', 'herse',
             'specifying', 'allow', 'keeps', 'order', 'longest', 'ha', 'help', "don't", 'furthering', 'indeed',
             'over', 'move', 'mainly', 'soon', 'years', 'course', 'through', 'looks', 'affect', 'fify', 'still',
             'its', 'before', 'member', 'group', 'thank', 'thence', 'selves', 'inward', 'actually', 'better',
             'willing', 'differently', 'thanx', 'ours', 'might', "haven't", 'then', 'non', 'good', 'somebody',
             'greater', 'thereby', 'downs', 'very', 'ownpart', "you've", 'they', 'not', 'false', 'now', 'nor',
             'instanceof', 'several', 'name', 'always', 'reasonably', 'whither', 'l', 'each', 'found', 'went',
             'higher', "mustn't", "isn't", 'mean', 'everyone', 'doing', 'eg', 'static', "we'd", 'ourselves',
             'year', 'et', 'beyond', "c's", 'out', 'large', 'shown', 'them', 'opened', 'twice', 'furthermore',
             'since', 'forty', 'looking', 're', 'seriously', "shouldn't", "they'll", 'got', 'myse', 'forth',
             'shows', 'regards', 'turning', "doesn't", 'differ', 'quite', 'whereupon', 'besides', 'x',
             'put', 'anyhow', 'wanted', '..', 'g', 'could', 'needing', 'hereupon', 'keep', 'thing', 'place',
             'w', 'ltd', 'hence', 'anyanyhowanyoneanythinganyway', 'onto', 'think', 'first', 'already',
             'seeming', 'thereafter', 'number', 'yourself', 'oursourselves', 'done', 'messag', 'another',
             'thick', 'open', 'between', 'awfully', "you're", 'given', "there's", 'indicate', 'ordering',
             'together', 'top', 'system', 'least', 'alsoalthoughalwaysamamong', 'anyone', 'their', 'too',
             'hundred', 'final', 'gives', 'interests', 'mostly', 'that', 'exactly', 'interesting', 'took',
             'immediate', 'part', 'somewhat', 'kept', 'believe', 'herself', 'than', 'specify', 'kind', 'b',
             'unfortunately', 'showed', 'gotten', 'older', 'see', 'nevertheless', 'r', 'were', 'toward',
             'introduc', 'are', 'and', 'sees', 'sometim', 'turned', 'few', 'say', 'unlikely', 'have', 'need',
             'seen', 'seem', 'obviously', 'saw', 'orders', 'relatively', 'caus', 'zero', 'thoroughly', 'latter',
             "i've", 'downwards', 'aside', 'thorough', 'also', 'without', 'take', 'which', 'wanting', 'wonder',
             'greatest', 'sure', 'unless', 'enum', 'shall', 'any', 'who', 'wells', "where's", 'most', 'said',
             'eight', 'but', 'nothing', 'why', 'parting', 'appear', 'cause', 'don', 'especially', 'nobody',
             'noone', 'sometimes', 'm', 'amoungst', 'face', "you'll", 'points', 'repli', "that's", 'normally',
             'came', 'saying', 'particularly', 'show', 'able', 'anyway', 'brief', 'protocol', 'find', 'fifth',
             'make', 'one', 'highest', 'true', 'less', 'outside', 'should', 'only', 'going', "here's",
             'pointed', 'do', 'his', 'goes', 'meanwhile', 'de', 'overall', 'sensible', 'truly', "they'd",
             'ones', 'nearly', 'despite', 'during', 'beings', 'him', 'areas', 'regarding', 'qv', 'h', 'cry',
             "wasn't", 'she', 'contain', "won't", 'where', 'greetings', 'ignored', 'we', "hasn't", 'namely',
             'computer', 'anyways', 'becaus', 'best', 'definitely', 'puts', 'ways', 'away', 'currently',
             'please', 'state', 'smallest', 'various', 'hopefully', 'probably', 'neither', 'across',
             'available', 'ends', 'men', 'opening', 'however', 'by', 'nd', 'interface', 'come', 'both', 'c',
             'last', 'many', "wouldn't", "he's", 'according', 'against', 'etc', 's', 'became', 'faces', 'com',
             'asked', 'comes', 'con', 'among', 'presumably', 'co', 'afterwards', 'point', 'seems', 'elevenelse',
             'whatever', 'furthered', 'alone', "couldn't", 'associated', 'accordingly', 'second', 'considering',
             'furthers', 'described', 'asks', "it's", 'three', 'been', 'whom', 'much', 'interest', 'hardly',
             'empty', 'wants', 'corresponding', 'fire', 'latterly', 'concerning', 'mine', 'assert', 'catch',
             'worked', 'an', 'hers', 'former', 'those', 'case', 'myself', 'novel', 'look', 'these', 'bill',
             'twenty', 'value', 'n', 'will', 'near', 'behavior', 'theres', 'seven', 'whereafter', '...',
             'almost', 'wherever', 'is', 'everywhere', 'thus', 'it', 'clearly', 'cant', 'someone', 'in',
             'return', 'ie', 'if', 'containing', 'null', 'inc', 'perhaps', 'things', 'began', 'same', 'wherein',
             'beside', 'parts', 'gets', "weren't", 'used', 'somewhere', 'upon', 'rout', 'uses', 'protected',
             "he'll", 'thoughts', 'implements', 'break', 'ours\tourselves', 'whereby', 'largely', 'i', 'whole',
             'well', 'anybody', 'finds', 'thought', 'exampl', "can't", 'y', 'the', 'otherwise', 'yours',
             'latest', 'lest', "she'll", 'newest', 'just', 'camel', 'being', 'generally', 'liked', 'backs',
             'front', 'rooms', 'using', 'facts', 'useful', 'yes', 'yet', 'unto', 'like', "we've", 'had',
             'except', 'default', 'lets', 'interested', 'extends', 'inner', 'input', 'has', 'ought', 'gave',
             'real', "t's", 'around', 'mayb', 'big', 'showing', "who's", 'possible', 'early', 'five', 'know',
             'amp', 'apart', 'moreover', 'hereafter', 'necessary', 'd', 'filenam', 'follows', 'server',
             'continue', 't', 'fully', 'become', 'works', 'grouping', 'therein', "why's", 'because', 'old',
             'often', 'some', 'back', 'self', 'towards', 'specified', 'himse', 'thinks', "shan't", 'happens',
             'throughout', 'for', 'bottom', 'though', 'per', 'wrong', 'everything', 'does', 'provides', 'tends',
             'reproduc', 'either', 'be', 'package', 'knew', 'backbebecame', 'seconds', 'of', 'nowhere',
             'although', 'output', 'sixty', 'super', 'entirely', 'on', 'about', 'goods', 'ok', 'would',
             'anything', 'getting', 'theirs', 'o', 'side', 'whence', 'plus', 'consequently', 'or', 'seeing',
             'own', 'formerly', 'twelve', 'into', 'within', 'due', 'down', 'appropriate', 'right', 'empti',
             'import', 'couldnt', 'your', 'behind', "how's", 'her', 'area', 'downed', 'there', 'question',
             'long', 'inasmuch', "we're", 'way', 'was', 'opens', 'himself', 'elsewhere', 'enough',
             'becoming', 'amongst', 'somehow', 'hi', 'ended', 'newer', 'trying', 'with', 'he', "they're",
             'throw', 'made', 'places', 'mrs', 'whether', 'wish', 'j', 'thickv', 'us', 'tell', 'placed',
             'below', 'un', 'native', "it'd", 'problem', 'z', 'clear', 'ex', 'gone', 'later', 'ordered',
             'creat', 'up', 'certain', 'abstract', 'describe', 'am', 'doesn', 'general', 'as', 'sometime',
             'exist', 'at', 'our', 'work', 'fill', 'again', 'hasnt', 'no', 'whereas', 'when', 'detail',
             'lately', 'grouped', 'other', 'you', 'really', "what's", 'nice', 'regardless', 'welcome',
             'problems', "let's", 'important', 'serious', 'else', 'sides', 'backing', 'younger', 'e', 'longer',
             'ending', 'backed', "she'd", 'hello', 'itself', 'transient', 'u', 'presenting', 'potenti', "she's",
             'once', 'having', 'evenly']

def write_file_a(file_path, content):
    with codecs.open(file_path, mode='a', encoding='utf-8') as file:
        file.write(content + "\n")

def write_search_log(content):
    file_path = "search_log_path/search_log.txt"
    with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
        file.write(content)
    file.close()

def read_search_log():
    file_path = "search_log_path/search_log"
    file = open(file_path, 'r')
    content = file.readline()
    file.close()
    return content

def get_mongo_connection():
    from com.mongodb import MongoClient
    from com.mongodb import DB
    from com.mongodb import DBCollection
    from com.mongodb import BasicDBObject
    from com.mongodb import DBObject
    mongoClient = MongoClient()
    db = mongoClient.getDB("Answers")
    return db

def camel_case_split(s):
    import re
    s = s.replace("_", " ")
    s1 = re.sub('(.)([A-Z][tmp-z]+)', r'\1 \2', s)
    s = re.sub('([tmp-z0-9])([A-Z])', r'\1 \2', s1).lower().replace("  ", " ").split()
    return s

def tokenize(s):
    import re
    return re.findall(r"[\w']+", s)

def unescape_html(s):
    from HTMLParser import HTMLParser
    p = HTMLParser()
    return p.unescape(s)

def get_code(s):
    code_snippets = []
    for item in s.split("</code>"):
        if "<code>" in item:
            code_tag = item [item.find("<code>")+len("<code>"):]
            if "." in code_tag and "(" in code_tag:
                code_tag = unescape_html(code_tag)
                code_snippets.append(code_tag)
    return code_snippets

def specialCharTokenizer(text):
    special_char_list = ['|', '=', '/', '(', ')', '[', ']', ',', '.', '_', '\'', '`', '!', '@', '#', '$', '%', '^', '&',
                         '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"', '\\']
    for s_char in special_char_list:
        text = text.replace(s_char, ' ')
    return text

def remove_code_block(s):
    from org.jsoup import Jsoup
    doc = Jsoup.parse(s)
    for element in doc.select("code"):
        element.remove()

    return doc.text()

def remove_html_tags(s):
    from org.jsoup import Jsoup
    return Jsoup.parse(s).text()

def so_text(s):
    from org.jsoup import Jsoup
    s = unescape_html(s)
    doc = Jsoup.parse(s)
    for element in doc.select("code"):
        element.remove()
    return doc.text()


java_stopwords = ["public", "private","protected", "interface", "abstract", "implements", "extends", "null", "new", "switch", "case", "default","synchronized", "do", "if", "else", "break","continue","this","assert" ,"for","instanceof", "transient", "final", "static" ,"void","catch","try", "throws","throw", "finally","return", "const" , "native", "super","while", "import", "package" ,"true", "false", "enum"]

def so_tokenizer(s, remove_html=True, as_str=True):
    if remove_html:
        from org.jsoup import Jsoup
        s = unescape_html(s)
        doc = Jsoup.parse(s)
        s = doc.text()
    tokens = tokenize(s)
    res = []
    for token in tokens:
        res.extend(camel_case_split(token))
        res.append(token.lower())
    res = [item for item in res if item not in java_stopwords]
    res = set(res)
    if as_str:
        return " ".join(res)
    else:
        return res

def copytree(src, dst, symlinks=False, ignore=None):
    import shutil
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def variable_type_map(source):
    import re
    from collections import defaultdict
    type_map = defaultdict("")
    parent = re.compile(r"\(\s*([^)]+?)\s*\)")
    for argumentlist in parent.findall(source):
        args = argumentlist.split(",")
        for arg in args:
            tokens = arg.split()
            if len(tokens) >= 2:
                type_map[tokens[-1]] = tokens[-2]
def md5(s):
    import hashlib
    return hashlib.md5(s).hexdigest()

def get_inline_and_block_code(s):
    code_snippets = set()
    for item in s.split("</code></pre>"):
        if "<pre><code>" in item:
            code_tag = item [item.find("<pre><code>")+len("<pre><code>"):]
            if "." in code_tag and "(" in code_tag:
                code_tag = unescape_html(code_tag)
                code_snippets.add(code_tag.strip())
    return code_snippets

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
    print('The path [%s] is not empty, we are cleaning the path..' % path)
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)






if __name__ == '__main__':
    pass
    # print camel_case_split("myFucking_CamelCase.7.9/66")
    # s = """
    # 	View.OnClickListener mStartButtonListener = new OnClickListener() {
    # 	@Override
    # 	public void onClick(View arg0) {
    # 		mChronometer.setBase(SystemClock.elapsedRealtime());
    # 		mChronometer.start();
    # 	}
    # };
    # """
    # print tokenize(s)
    # print so_tokenizer(s, remove_html=False)
def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        return loaded_object

def getClassNames(class_name_file):
    class_names = list()
    classes_contents = read_file(class_name_file)
    for line in classes_contents.splitlines():
        class_names.append(line.split('.')[0])
    return class_names

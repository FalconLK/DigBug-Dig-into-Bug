#-*- coding: utf-8 -*-
import os, codecs, shutil

my_stop_words = ['', 'secondly', 'all', 'gt', 'consider', 'pointing', 'whoever', 'global', 'felt', 'four', 'edu',
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
                 'long',  'inasmuch', "we're", 'way', 'was', 'opens', 'himself', 'elsewhere', 'enough',
                 'becoming', 'amongst', 'somehow', 'hi', 'ended', 'newer', 'trying', 'with', 'he', "they're",
                 'throw', 'made', 'places', 'mrs', 'whether', 'wish', 'j', 'thickv', 'us', 'tell', 'placed',
                 'below', 'un', 'native', "it'd", 'problem', 'z', 'clear', 'ex', 'gone', 'later', 'ordered',
                 'creat', 'up', 'certain', 'abstract', 'describe', 'am', 'doesn', 'general', 'as', 'sometime',
                 'exist', 'at', 'our', 'work', 'fill', 'again', 'hasnt', 'no', 'whereas', 'when', 'detail',
                 'lately', 'grouped', 'other', 'you', 'really', "what's", 'nice', 'regardless', 'welcome',
                 'problems', "let's", 'important', 'serious', 'else', 'sides', 'backing', 'younger', 'e', 'longer',
                 'ending', 'backed', "she'd", 'hello', 'itself', 'transient', 'u', 'presenting', 'potenti', "she's",
                 'once', 'having', 'evenly']

def truncate_search_log():
    file_path = "/Users/Falcon/PycharmProjects/CoCaBu_remote/GitSearch/FrontEnd/static/search_log"
    file = open(file_path, 'w')
    file.truncate()
    file.close()

def write_file_a(file_path, content):
    with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
        file.write(content + "\n")

def write_search_log(content):
    file_path = "/Users/Falcon/PycharmProjects/CoCaBu_remote/GitSearch/FrontEnd/static/search_log"
    with codecs.open(file_path, mode='tmp', encoding='utf-8') as file:
        #encodedContent = unicode(content, encoding=u'euc-kr').encode(encoding='utf-8')
        file.write(content)  #encodedContent)
    file.close()


def read_search_log():
    file_path = "/Users/Falcon/PycharmProjects/CoCaBu_remote/GitSearch/FrontEnd/static/search_log"
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
    """ Removes code tag and its content from SO body as well as all html tags"""
    from org.jsoup import Jsoup
    s = unescape_html(s)
    doc = Jsoup.parse(s)
    for element in doc.select("code"):
        element.remove()

    return doc.text()


java_stopwords = ["public", "private","protected", "interface", "abstract", "implements", "extends", "null", "new", "switch", "case", "default","synchronized", "do", "if", "else", "break","continue","this","assert" ,"for","instanceof", "transient", "final", "static" ,"void","catch","try", "throws","throw", "finally","return", "const" , "native", "super","while", "import", "package" ,"true", "false", "enum",
'', "don't", 'some', 'year', 'your', 'without', 'via', 'these', 'would', 'because', 'near', 'ten', ' ', 'unlikely', "he'll", 'thus', 'meanwhile', 'younger', 'viz', 'yourselves', 'contains', 'downed', 'eleven', 'detail', 'much', 'appropriate', 'anybody', 'least', "why's", 'turn', 'example', 'same', 'after', "shouldn't", "you've", "we'd", 'ordered', 'tmp', "wouldn't", 'b', 'c', 'thanx', 'd', 'e', 'f', 'namely', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'the', 'newer', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'fifth', 'thank', 'y', 'z', 'faces', 'yours', 'novel', 'nine', 'got', 'good', 'empty', 'wish', "how's", 'besides', 'serious', 'others', 'elevenelse', 'area', "t's", 'making', 'need', 'its', 'often', 'onto', 'gone', 'aside', 'therefore', 'hardly', 'useful', 'ours\tourselves', 'furthers', 'young', 'downwards', 'smallest', 'myse', "c's", 'nowhere', 'sorry', 'provides', "you're", 'end', 'forty', "we'll", 'room', 'better', 'with', 'there', 'well', 'happens', 'tries', 'smaller', 'wanting', 'years', 'turns', 'number', 'tried', 'per', "when's", 'order', 'bottombut', 'went', 'considering', 'nothing', 'anyhow', 'specify', 'forth', 'ever', "we've", 'system', 'even', 'orders', 'presenting', 'thats', 'other', 'hundred', 'indicated', 'against', 'respectively', "tmp's", "isn't", "hadn't", 'howbeit', 'asked', 'top', 'too', 'indicates', 'have', 'ownpart', 'accordingly', 'furthering', 'particularly', 'thoroughly', 'awfully', "ain't", 'oursourselves', 'com', 'con', 'almost', 'lets', 'amoungst', 'upon', 'points', 'latterly', 'amongst', 'etc', 'whether', 'members', 'quite', 'all', 'always', 'new', 'took', 'below', 'already', 'everyone', "didn't", 'lest', 'shall', 'less', 'were', "we're", 'try', 'became', 'cause', 'around', 'and', 'today', 'working', 'saying', 'says', 'fifteen', 'whence', 'cry', 'followed', 'despite', 'any', 'opening', 'until', 'interested', 'formerly', 'gotten', 'thought', 'anywhere', 'wherein', "wasn't", "where's", 'worked', 'differently', 'let', 'state', 'thinks', 'welcome', 'fully', 'using', 'began', 'containing', 'want', 'each', 'specifying', 'himself', 'wanted', 'must', 'maybe', 'probably', 'another', 'furthered', 'two', 'facts', 'anyway', 'found', 'are', 'does', 'taken', 'came', 'where', 'gives', 'latest', 'think', 'entirely', '...', 'call', 'such', 'ask', 'describe', 'thing', 'through', "won't", 'anyways', 'becoming', 'goods', 'needing', 'had', 'cant', 'either', 'ours', 'things', 'yourself', 'has', 'newest', 'those', "they'd", 'seeming', 'given', 'last', "let's", 'might', 'whatever', 'longer', 'everywhere', 'name', 'overall', 'full', 'next', 'away', 'asking', 'nearly', 'show', 'becausebecomebecomes', 'non', 'anything', 'nor', 'not', 'now', 'ends', 'hence', 'early', 'thoughts', 'unto', 'yes', 'was', 'yet', "i'll", 'way', 'inasmuch', 'what', 'furthermore', 'when', 'three', 'put', 'her', 'whoever', 'largely', 'far', 'truly', 'greater', 'case', "it'll", 'okay', 'evenly', 'give', 'having', 'grouping', 'hereupon', 'himse', 'noone', "she'd", 'youngest', "mustn't", 'couldnt', 'computer', 'ways', "she's", 'older', 'merely', 'more', 'unfortunately', 'lately', 'great', 'beings', 'parted', 'sides', 'interests', 'certain', 'small', 'before', 'tell', 'used', 'him', 'looks', 'his', 'shows', 'presented', 'few', 'pointing', 'consider', 'keeps', 'described', 'group', 'otherwise', "you'd", 'whither', 'thickv', "it's", 'kind', 'particular', 'opened', 'inner', 'done', 'both', 'most', 'important', 'twice', 'parting', 'outside', 'keep', "it'd", 'who', 'part', 'why', 'their', 'elsewhere', 'point', 'general', 'alone', 'along', 'ltd', 'amount', 'move', 'hereafter', 'saw', 'clear', 'also', 'say', 'enough', 'gets', 'differ', 'someone', 'third', 'mean', 'various', 'neither', 'latter', 'uses', 'further', 'front', 'sometime', 'been', 'mostly', 'hasnt', "couldn't", 'areas', 'appreciate', 'finds', "doesn't", 'you', 'afterwards', 'sure', 'going', 'bill', 'am', 'an', 'whose', 'former', 'mill', 'as', 'at', 'trying', 'turning', 'looking', "i've", 'be', 'ordering', 'comes', 'consequently', 'how', 'see', 'inward', 'by', 'whom', 'indicate', 'mine', 'sixty', 'contain', 'right', 'possible', 'co', 'somewhat', 'under', 'did', 'de', 'rooms', 'sometimes', 'backbebecame', 'do', 'itse', 'down', 'later', 'needs', 'which', 'ignored', 'eg', 'thereafter', 'regarding', 'et', 'she', 'never', 'take', 'ex', 'immediate', 'parts', 'relatively', "aren't", 'little', 'however', 'some', 'rather', 'for', 'back', 'greetings', 'states', 'getting', 'perhaps', 'just', 'over', 'six', 'thence', 'go', 'obviously', 'kept', 'although', 'selves', 'fify', 'he', 'showing', 'presents', 'hi', 'very', 'big', 'placed', 'therein', 'soon', 'thick', 'thanks', 'else', 'four', 'beside', 'usually', 'whereas', 'ie', 'if', "there's", 'likely', 'large', 'in', 'made', 'is', 'it', 'being', 'somebody', "weren't", 'asks', 'gave', 'opens', 'hello', 'whereby', 'secondly', 'become', 'longest', 'works', 'turned', 'whereupon', 'eight', 'theres', 'known', 'member', 'hopefully', 'man', 'everything', "can't", 'together', 'knows', 'twenty', 'side', 'may', 'seemed', 'within', 'could', 'knew', 'off', 'generally', 'places', 'alsoalthoughalwaysamamong', 'able', 'theirs', 'presumably', 'use', 'several', 'while', 'liked', 'second', 'that', 'high', 'find', 'than', 'me', 'different', 'insofar', 'regardless', 'downs', 'mr', 'follows', 'seriously', 'my', 'fill', 'plus', 'becomes', 'nd', 'present', 'since', 'problems', '..', 'no', 'behind', 'best', 'herse', 'hither', 'of', 'men', 'oh', 'somehow', 'ok', 'make', 'on', 'allows', 'brief', 'certainly', 'or', 'interesting', 'exactly', "c'mon", 'concerning', 'due', 'backs', 'about', "what's", 'somewhere', "haven't", 'above', 'downing', 'fire', 'they', "here's", 'grouped', 'qv', 'old', 'myself', 'herein', 'them', 'then', 'something', 'anyanyhowanyoneanythinganyway', 'pointed', 'rd', 're', 'thereby', 'highest', 'twelve', 'except', 'sincere', 'sub', 'nevertheless', 'fact', "hasn't", 'believe', 'seen', 'long', 'seem', 'sup', 'into', 'unless', 'so', 'apart', 'ought', 'necessary', 'though', 'one', 'thorough', 'many', 'actually', 'appear', 'face', 'definitely', 'th', 'oldest', 'associated', 'showed', 'to', 'open', "they've", 'but', 'willing', 'available', 'numbers', 'seven', 'mainly', 'zero', 'whenever', 'un', 'up', 'five', 'us', 'beforehand', 'this', 'felt', 'please', 'reasonably', 'look', 'thin', 'especially', 'once', 'sees', 'know', 'vs', 'higher', 'allow', 'que', 'doing', 'needed', 'changes', "that's", 'we', 'backing', 'interest', 'themselves', 'throughout', "he's", 'wants', 'wonder', 'every', "they're", 'cases', 'again', "he'd", 'indeed', 'ones', 'backed', 'whole', 'during', 'none', 'beyond', "she'll", 'seconds', 'problem', 'nobody', 'between', 'still', 'work', 'come', "they'll", 'itself', 'toward', 'among', 'anyone', 'following', "i'd", 'our', 'ourselves', "i'm", 'specified', 'out', 'across', 'seeing', 'moreover', 'causes', 'get', 'course', 'place', 'sensible', 'wherever', 'mrs', 'puts', 'help', 'ended', 'self', 'cannot', 'hereby', 'whereafter', 'first', 'thru', 'own', 'clearly', 'only', 'should', 'from', "you'll", 'like', 'goes', 'bottom', 'towards', 'regards', 'sent', 'ending', 'edu', 'herself', 'seems', 'thereupon', 'here', 'everybody', 'according', "shan't", 'hers', 'can', "who's", 'wells', 'said', 'value', 'inc', 'greatest', 'will', 'groups', 'instead', 'really', 'currently', 'corresponding', 'tends', 'normally', 'nice', 'we', 'when', 'where', 'tr', 'gt', 'so', 'would', 'like', 'will', 'it', 'have', 'which', 'all', 'doesn', 'don', 'sometim', 'behavior', 'ha', 'introduc', 'potenti', 'break', 'exist', 'cannot', 'repli', 'except', 'output', 'input', 'rout', 'public', 'txt', 'wrong', 'filenam', 'can', 'question', 'how', 'other', 'mayb', 'see', 'look', 'most', 'list', 'protocol', 'empti', 'server', 'becaus', 'affect', 'doe', 'messag', 'global', 'creat', 'reproduc', '',"don't", 'some', 'year', 'your', 'without', 'via', 'these', 'would', 'because', 'near', 'ten', ' ', 'unlikely', "he'll", 'thus', 'meanwhile', 'younger', 'viz', 'yourselves', 'contains', 'downed', 'eleven', 'detail', 'much', 'appropriate', 'anybody', 'least', "why's", 'turn', 'example', 'same', 'after', "shouldn't", "you've", "we'd", 'ordered', 'tmp', "wouldn't", 'b', 'c', 'thanx', 'd', 'e', 'f', 'namely', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'the', 'newer', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'fifth', 'thank', 'y', 'z', 'faces', 'yours', 'novel', 'nine', 'got', 'good', 'empty', 'wish', "how's", 'besides', 'serious', 'others', 'elevenelse', 'area', "t's", 'making', 'need', 'its', 'often', 'onto', 'gone', 'aside', 'therefore', 'hardly', 'useful', 'ours\tourselves', 'furthers', 'young', 'downwards', 'smallest', 'myse', "c's", 'nowhere', 'sorry', 'provides', "you're", 'end', 'forty', "we'll", 'room', 'better', 'with', 'there', 'well', 'happens', 'tries', 'smaller', 'wanting', 'years', 'turns', 'number', 'tried', 'per', "when's", 'order', 'bottombut', 'went', 'considering', 'nothing', 'anyhow', 'specify', 'forth', 'ever', "we've", 'system', 'even', 'orders', 'presenting', 'thats', 'other', 'hundred', 'indicated', 'against', 'respectively', "tmp's", "isn't", "hadn't", 'howbeit', 'asked', 'top', 'too', 'indicates', 'have', 'ownpart', 'accordingly', 'furthering', 'particularly', 'thoroughly', 'awfully', "ain't", 'oursourselves', 'com', 'con', 'almost', 'lets', 'amoungst', 'upon', 'points', 'latterly', 'amongst', 'etc', 'whether', 'members', 'quite', 'all', 'always', 'new', 'took', 'below', 'already', 'everyone', "didn't", 'lest', 'shall', 'less', 'were', "we're", 'try', 'became', 'cause', 'around', 'and', 'today', 'working', 'saying', 'says', 'fifteen', 'whence', 'cry', 'followed', 'despite', 'any', 'opening', 'until', 'interested', 'formerly', 'gotten', 'thought', 'anywhere', 'wherein', "wasn't", "where's", 'worked', 'differently', 'let', 'state', 'thinks', 'welcome', 'fully', 'using', 'began', 'containing', 'want', 'each', 'specifying', 'himself', 'wanted', 'must', 'maybe', 'probably', 'another', 'furthered', 'two', 'facts', 'anyway', 'found', 'are', 'does', 'taken', 'came', 'where', 'gives', 'latest', 'think', 'entirely', '...', 'call', 'such', 'ask', 'describe', 'thing', 'through', "won't", 'anyways', 'becoming', 'goods', 'needing', 'had', 'cant', 'either', 'ours', 'things', 'yourself', 'has', 'newest', 'those', "they'd", 'seeming', 'given', 'last', "let's", 'might', 'whatever', 'longer', 'everywhere', 'name', 'overall',  'full', 'next', 'away', 'asking', 'nearly', 'show', 'becausebecomebecomes', 'non', 'anything', 'nor', 'not', 'now', 'ends', 'hence', 'early', 'thoughts', 'unto', 'yes', 'was', 'yet', "i'll", 'way', 'inasmuch', 'what', 'furthermore', 'when', 'three', 'put', 'her', 'whoever', 'largely', 'far', 'truly', 'greater', 'case', "it'll", 'okay', 'evenly', 'give', 'having', 'grouping', 'hereupon', 'himse', 'noone', "she'd", 'youngest', "mustn't", 'couldnt', 'computer', 'ways', "she's", 'older', 'merely', 'more', 'unfortunately', 'lately', 'great', 'beings', 'parted', 'sides', 'interests', 'certain', 'small', 'before', 'tell', 'used', 'him', 'looks', 'his', 'shows', 'presented', 'few', 'pointing', 'consider', 'keeps', 'described', 'group', 'otherwise', "you'd", 'whither', 'thickv', "it's", 'kind', 'particular', 'opened', 'inner', 'done', 'both', 'most', 'important', 'twice', 'parting', 'outside', 'keep', "it'd", 'who', 'part', 'why', 'their', 'elsewhere', 'point', 'general', 'alone', 'along', 'ltd', 'amount', 'move', 'hereafter', 'saw', 'clear', 'also', 'say', 'enough', 'gets', 'differ', 'someone', 'third', 'mean', 'various', 'neither', 'latter', 'uses', 'further', 'front', 'sometime', 'been', 'mostly', 'hasnt', "couldn't", 'areas', 'appreciate', 'finds', "doesn't", 'you', 'afterwards', 'sure', 'going', 'bill', 'am', 'an', 'whose', 'former', 'mill', 'as', 'at', 'trying', 'turning', 'looking', "i've", 'be', 'ordering', 'comes', 'consequently', 'how', 'see', 'inward', 'by', 'whom', 'indicate', 'mine', 'sixty', 'contain', 'right', 'possible', 'co', 'somewhat', 'under', 'did', 'de', 'rooms', 'sometimes', 'backbebecame', 'do', 'itse', 'down', 'later', 'needs', 'which', 'ignored', 'eg', 'thereafter', 'regarding', 'et', 'she', 'never', 'take', 'ex', 'immediate', 'parts', 'relatively', "aren't", 'little', 'however', 'some', 'rather', 'for', 'back', 'greetings', 'states', 'getting', 'perhaps', 'just', 'over', 'six', 'thence', 'go', 'obviously', 'kept', 'although', 'selves', 'fify', 'he', 'showing', 'presents', 'hi', 'very', 'big', 'placed', 'therein', 'soon', 'thick', 'thanks', 'else', 'four', 'beside', 'usually', 'whereas', 'ie', 'if', "there's", 'likely', 'large', 'in', 'made', 'is', 'it', 'being', 'somebody', "weren't", 'asks', 'gave', 'opens', 'hello', 'whereby', 'secondly', 'become', 'longest', 'works', 'turned', 'whereupon', 'eight', 'theres', 'known', 'member', 'hopefully', 'man', 'everything', "can't", 'together', 'knows', 'twenty', 'side', 'may', 'seemed', 'within', 'could', 'knew', 'off', 'generally', 'places', 'alsoalthoughalwaysamamong', 'able', 'theirs', 'presumably', 'use', 'several', 'while', 'liked', 'second', 'that', 'high', 'find', 'than', 'me', 'different', 'insofar', 'regardless', 'downs', 'mr', 'follows', 'seriously', 'my', 'fill', 'plus', 'becomes', 'nd', 'present', 'since', 'problems', '..', 'no', 'behind', 'best', 'herse', 'hither', 'of', 'men', 'oh', 'somehow', 'ok', 'make', 'on', 'allows', 'brief', 'certainly', 'or', 'interesting', 'exactly', "c'mon", 'concerning', 'due', 'backs', 'about', "what's", 'somewhere', "haven't", 'above', 'downing', 'fire', 'they', "here's", 'grouped', 'qv', 'old', 'myself', 'herein', 'them', 'then', 'something', 'anyanyhowanyoneanythinganyway', 'pointed', 'rd', 're', 'thereby', 'highest', 'twelve', 'except', 'sincere', 'sub', 'nevertheless', 'fact', "hasn't", 'believe', 'seen', 'long', 'seem', 'sup', 'into', 'unless', 'so', 'apart', 'ought', 'necessary', 'though', 'one', 'thorough', 'many', 'actually', 'appear', 'face', 'definitely', 'th', 'oldest', 'associated', 'showed', 'to', 'open', "they've", 'but', 'willing', 'available', 'numbers', 'seven', 'mainly', 'zero', 'whenever', 'un', 'up', 'five', 'us', 'beforehand', 'this', 'felt', 'please', 'reasonably', 'look', 'thin', 'especially', 'once', 'sees', 'know', 'vs', 'higher', 'allow', 'que', 'doing', 'needed', 'changes', "that's", 'we', 'backing', 'interest', 'themselves', 'throughout', "he's", 'wants', 'wonder', 'every', "they're", 'cases', 'again', "he'd", 'indeed', 'ones', 'backed', 'whole', 'during', 'none', 'beyond', "she'll", 'seconds', 'problem', 'nobody', 'between', 'still', 'work', 'come', "they'll", 'itself', 'toward', 'among', 'anyone', 'following', "i'd", 'our', 'ourselves', "i'm", 'specified', 'out', 'across', 'seeing', 'moreover', 'causes', 'get', 'course', 'place', 'sensible', 'wherever', 'mrs', 'puts', 'help', 'ended', 'self', 'cannot', 'hereby', 'whereafter', 'first', 'thru', 'own', 'clearly', 'only', 'should', 'from', "you'll", 'like', 'goes', 'bottom', 'towards', 'regards', 'sent', 'ending', 'edu', 'herself', 'seems', 'thereupon', 'here', 'everybody', 'according', "shan't", 'hers', 'can', "who's", 'wells', 'said', 'value', 'inc', 'greatest', 'will', 'groups', 'instead', 'really', 'currently', 'corresponding', 'tends', 'normally']

def so_tokenizer(s, remove_html=True, as_str=True):
    if remove_html:
        from org.jsoup import Jsoup
        s = unescape_html(s)
        doc = Jsoup.parse(s)
        s = doc.text()
    tokens = tokenize(s)
    # tokens = set(tokens)

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

    # Deduce types from method declaration
    parent = re.compile(r"\(\s*([^)]+?)\s*\)")
    for argumentlist in parent.findall(source):
        args = argumentlist.split(",")
        for arg in args:
            tokens = arg.split()
            if len(tokens) >= 2:
                type_map[tokens[-1]] = tokens[-2]

    # Deduce types from variable declartion

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


def remove_unified_stop_lists(unified_query):
    # TODO : Stop Keyword in here!
    stop_list = [
        'typed_method_call:Log.e',
        'typed_method_call:Log.i',
        'typed_method_call:Log.d',
        'typed_method_call:System.exit',
        'typed_method_call:PrintStream.println',

        'used_classes:void',
        'used_classes:int',
        'used_classes:List',
        'used_classes:byte[]',
        'used_classes:java',
        'used_classes:Object',
        'used_classes:Global',
        'used_classes:int',
        'used_classes:char',
        'used_classes:float',
        'used_classes:double',
        'used_classes:byte',
        'used_classes:long',
        'used_classes:T',
        'used_classes:short',
        'used_classes:System',
        'used_classes:PrintStream',
        'used_classes:byte\[\]',
        'used_classes:java.io',
        'used_classes:Exception',
        'used_classes:java.io',
        'used_classes:org',
        'used_classes:org.apache',
        'used_classes:org.apache.camel',
        'used_classes:org.apache.camel.component',
        'used_classes:org.apache.camel.tableBuilder',
        'used_classes:org.junit',
        'used_classes:org.apache.camel.component.mock',
        'used_classes:org.apache.camel.test',
        'used_classes:org.apache.camel.impl',
        'used_classes:org.apache.camel.util',
        'used_classes:org.apache.camel.test.junit4',
        'used_classes:javax',
        'used_classes:Thread',
        'used_classes:LOG',
        'used_classes:IllegalArgumentException',
        'used_classes:com',
        'used_classes:METHOD',

        'methods_called:main',
        'methods_called:write',
        'methods_called:close',
        'methods_called:from',
        'methods_called:println',
        'methods_called:close',
        'methods_called:mkdir',
        'methods_called:exists',
        'methods_called:println',
        'methods_called:print',
        'methods_called:size',
        'methods_called:compareTo',
        'methods_called:newInstance',

        'unresolved_method_calls:out.println',

        'methods:write',
        'methods:main',
        'methods:OR',
        'methods:AND',
        'methods:NOT',
        'methods:invalid_argument',

        'used_classes:CREATE'
        'used_classes:AND',
        'used_classes:NOT',
        'used_classes:OR',
        'used_classes:FROM',
        'used_classes:WHERE',
        'used_classes:SELECT',
        'used_classes:JOIN',
        'used_classes:ON',
        'used_classes:REFERENCES',
        'used_classes:GOTO',
        'used_classes:GRANT',
        'used_classes:GROUP',
        'used_classes:HAVING',
        'used_classes:BY',
        'used_classes:RESTRICT',
        'used_classes:DISTINCT',
        'used_classes:REVOKE',
        'used_classes:RETURN',
        'used_classes:SCHEMA',
        'used_classes:DROP',
        'used_classes:ORDER',

        'code_hints:NULL',
        'code_hints:UNIQUE',
        'code_hints:PRIMARY',
        'code_hints:NOT',
        'code_hints:KEY',
        'code_hints:OR',
        'code_hints:FOUR',

        'literals:ouch\!',
        'literals:About',
        'literals:About to read',



        'code:org',
        'code:apach',
        'code:hadoop',
        'code:hbase',
        'code:reader',
        'code:listen',
        'code:count',
        'code:util',
        'code:warn',
        'code:read',
        'code:doread',
        'code:data',
        'code:code',
        'code:fal',
        'code:success',
        'code:howev',
        'code:thi',
        'code:slowli',
        'code:onli',
        'code:file',
        'code:befor',
        'code:method',
        'code:anyth',
        'code:main',
        'code:object',
        'code:fail',
        'code:string',
        'code:error'
        'code:file',
        'code:alwai',
        'code:relat',
        'code:tri',
        'code:multipl',
        'code:time',
        'code:mani',
        'code:log',

    ]
    splited_unified_query = unified_query.split()
    query = ""

    # import re
    # def hasNumbers(inputString):
    #     return bool(re.search(r'\d', inputString))
    #
    for structured_query in splited_unified_query:
        # if not structured_query in stop_list and not hasNumbers(structured_query):
        if not structured_query in stop_list:
            query += structured_query + " "



    return query

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
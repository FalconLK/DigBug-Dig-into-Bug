#-*- coding: utf-8 -*-
# from __future__ import print_function

# import re, sys, html, os, HTMLParser    #Python2 (서버)
from html.parser import HTMLParser    #Python3 (요청)

import sys, re, os, html
sys.path.append(".")
sys.path.append("..")
sys.path.append("...")
sys.path.append('/home/ubuntu/Desktop/jython-2.7.0/Lib/site-packages/nltk/')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from string import punctuation

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
                 'long', 'inasmuch', "we're", 'way', 'was', 'opens', 'himself', 'elsewhere', 'enough',
                 'becoming', 'amongst', 'somehow', 'hi', 'ended', 'newer', 'trying', 'with', 'he', "they're",
                 'throw', 'made', 'places', 'mrs', 'whether', 'wish', 'j', 'thickv', 'us', 'tell', 'placed',
                 'below', 'un', 'native', "it'd", 'problem', 'z', 'clear', 'ex', 'gone', 'later', 'ordered',
                 'creat', 'up', 'certain', 'abstract', 'describe', 'am', 'doesn', 'general', 'as', 'sometime',
                 'exist', 'at', 'our', 'work', 'fill', 'again', 'hasnt', 'no', 'whereas', 'when', 'detail',
                 'lately', 'grouped', 'other', 'you', 'really', "what's", 'nice', 'regardless', 'welcome',
                 'problems', "let's", 'important', 'serious', 'else', 'sides', 'backing', 'younger', 'e', 'longer',
                 'ending', 'backed', "she'd", 'hello', 'itself', 'transient', 'u', 'presenting', 'potenti', "she's",
                 'once', 'having', 'evenly',

                 "#", "(", ")", "?", "/", "\"", "'ll", "'ve", "-", "tmp's", "able", "about", "above", "abroad", "abst",
                 "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "adopted",
                 "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ago", "ah", "ahead",
                 "ain't", "all", "allow", "allows", "almost", "alone", "along", "alongside", "already", "also",
                 "although", "always", "am", "amid", "amidst", "among", "amongst", "an", "and", "announce", "another",
                 "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apart",
                 "apparently", "appear", "appreciate", "appropriate", "approximately", "are", "aren", "aren't", "arent",
                 "arise", "around", "as", "aside", "ask", "asking", "associated", "at", "auth", "available", "away",
                 "awfully", "back", "backward", "backwards", "be", "became", "because", "become", "becomes", "becoming",
                 "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being",
                 "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "biol", "both",
                 "brief", "briefly", "but", "by", "c'mon", "c's", "ca", "came", "can", "can't", "cannot", "cant",
                 "caption", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "co.", "com", "come",
                 "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains",
                 "corresponding", "could", "couldn't", "couldnt", "course", "currently", "dare", "daren't", "date",
                 "definitely", "described", "despite", "did", "didn't", "different", "directly", "do", "does", "doesn't",
                 "doing", "don't", "done", "down", "downwards", "due", "during", "each", "ed", "edu", "effect", "eg",
                 "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "entirely", "especially",
                 "et", "et-al", "etc", "even", "ever", "evermore", "every", "everybody", "everyone", "everything",
                 "everywhere", "ex", "exactly", "example", "except", "fairly", "far", "farther", "few", "fewer", "ff",
                 "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "forever", "former",
                 "formerly", "forth", "forward", "found", "four", "from", "further", "furthermore", "gave", "get",
                 "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "going", "gone", "got", "gotten",
                 "greetings", "had", "hadn't", "half", "happens", "hardly", "has", "hasn't", "have", "haven't",
                 "having", "he", "he'd", "he'll", "he's", "hed", "hello", "help", "hence", "her", "here", "here's",
                 "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him",
                 "himself", "his", "hither", "home", "hopefully", "how", "how's", "howbeit", "however", "hundred", "i'd", "i'll", "i'm", "i've", "id", "ie", "if", "ignored", "im", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "inc.", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "inside", "insofar", "instead", "into", "invention", "inward", "is", "isn't", "it", "it'd", "it'll", "it's", "itd", "its", "itself", "just", "keep", "keeps", "kept", "keys", "kg", "km", "know", "known", "knows", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "let's", "lets", "like", "liked", "likely", "likewise", "line", "little", "look", "looking", "looks", "low", "lower", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mayn't", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn't", "million", "mine", "minus", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "mustn't", "my", "myself", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needn't", "needs", "neither", "never", "neverf", "neverless", "nevertheless", "new", "next", "nine", "ninety", "no", "no-one", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "notwithstanding", "novel", "now", "nowhere", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "one's", "ones", "only", "onto", "opposite", "or", "ord", "other", "others", "otherwise", "ought", "oughtn't", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provided", "provides", "put", "que", "quickly", "quite", "qv", "ran", "rather", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "round", "run", "said", "same", "saw", "say", "saying", "says", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "shan't", "she", "she'd", "she'll", "she's", "shed", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "someday", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "state", "states", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "t's", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "that's", "that've", "thats", "the", "The", "their", "theirs", "them", "themselves", "then", "thence", "there", "there'd", "there'll", "there're", "there's", "there've", "thereafter", "thereby", "thered", "therefore", "therein", "thereof", "therere", "theres", "thereto", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "theyd", "theyre", "thing", "things", "think", "third", "thirty", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "til", "till", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "un", "under", "underneath", "undoing", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "upwards", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "value", "various", "versus", "very", "via", "viz", "vol", "vols", "vs", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've", "wed", "welcome", "well", "went", "were", "weren't", "what", "what'll", "what's", "what've", "whatever", "whats", "when", "when's", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "whichever", "while", "whilst", "whim", "whither", "who", "who'd", "who'll", "who's", "whod", "whoever", "whole", "whom", "whomever", "whos", "whose", "why", "why's", "widely", "will", "willing", "wish", "with", "within", "without", "won't", "wonder", "words", "world", "would", "wouldn't", "www", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "youd", "your", "youre", "yours", "yourself", "yourselves", "zero", "﻿I", "﻿a", "﻿able",
                'java', 'abstract', 'default', 'if', 'package', 'synchronized', 'assert', 'do', 'implements', 'private', 'this', 'double', 'import', 'protected', 'throw', 'break', 'else', 'instanceof', 'public', 'throws', 'byte', 'extends', 'int', 'return', 'transient', 'case', 'false', 'interface', 'short', 'true', 'catch', 'final', 'long', 'static', 'try', 'char', 'finally', 'native', 'strictfp', 'void',  'float', 'new', 'super', 'volatile', 'const', 'for', 'null', 'switch', 'while', 'continue', 'goto', 'byvalue', 'future', 'generic', 'inner', 'operator', 'outer', 'rest', 'var', 'volatile', 'assert',
                'true', 'test', 'lt', 'special'
                 ]

en_stop = stopwords.words('english')
progress = 0


def handleUnderScore(token_list):
    token_list = getTokens(token_list)
    underScored = list()
    for i in token_list:
        listOfCC = i.split('_')
        underScored.extend(listOfCC)
        if i not in listOfCC:
            underScored.append(i)
    return underScored

def getTokens(re):
    #tokenizer = RegexpTokenizer(r'\w+')
    tokenizer = RegexpTokenizer(r'\S+')
    tokens = tokenizer.tokenize(re)
    # tokens = preSpecialCharRemove(str(tokens))
    return tokens

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[tmp-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][tmp-z])|$)', identifier)
    res = [m.group(0) for m in matches]
    return res

def removeEndingPunct(token_list):
    stripped = [i.strip(punctuation) for i in token_list]
    return str(stripped)

def charLength(x, l=3):
    if x.isalpha() and len(x) >= l:
        return True
    else:
        return False

# def preSpecialCharRemove(tokens):
#     retrieved = list()
#     special_char_list = ['//', '|', '=', '/', '(', ')', '[', ']', ',', '.', '_', '\'', '`', '!', '@', '#', '$', '%', '^', '&', '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"', '\\']
#     for word in tokens:
#         for s_char in special_char_list:
#             if s_char in word:
#                 word = word.replace(s_char, ' ')
#         if word == ' ':
#             continue
#         retrieved.append(word.strip())
#     return retrieved

def preSpecialCharRemove(text):
    special_char_list = ['|', '=', '/', '(', ')', '[', ']', ',', '.', '\'', '`', '!', '@', '#', '$', '%', '^', '&',
                         '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"', '\\', '~']
    for s_char in special_char_list:
        text = text.replace(s_char, ' ')

    return text

def handleCamelCase(tokens):
    camelCased = list()
    # token_list = getTokens(text)
    for i in tokens:
        listOfCC = camel_case_split(i)
        camelCased.extend(listOfCC)
    # text = " ".join(camelCased)
    return camelCased

def stem(tokens):
    # tokens = getTokens(text)
    p_stemmer = PorterStemmer()
    stemmed_tokens = [p_stemmer.stem(i) for i in tokens]
    # text = " ".join(stemmed_tokens)
    return stemmed_tokens

def preStopRemoval(tokens):
    # tokenlist = getTokens(text)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in my_stop_words]
    # text = " ".join(stopped_tokens)
    return stopped_tokens

def lower_(tokens):
    # token_list = getTokens(text)
    lowered_tokens = [i.lower() for i in tokens]
    # text = " ".join(lower)
    return lowered_tokens


'''
Basic
    0. Convert all named and numeric character references (e.g., &gt;) in the string to the corresponding Unicode characters) by following HTML5 standard
    1. tokenization by the white space
    2. ending punctuation removal
    4. digit removal
    5. char length < 2, then exclude
'''

'''
Kinds
    [B] baseline
    [SPC] split by special char
    [CMC] split by camel case
    [STM] stemming
    [SWR] stop words removal 
'''

def preBasic(text):
    # text = HTMLParser.HTMLParser().unescape(text)   # Indexing 및 Server 실행 시
    text = html.unescape(text)    # Request 시

    # tokens = getTokens(text)
    return text

def SPC(text):
    # text = lower_(tokens)
    return preSpecialCharRemove(text)

def CMC(tokens):
    text = handleCamelCase(tokens)
    return lower_(text)

def STM(tokens):
    text = lower_(tokens)
    return stem(text)

def SWR(tokens):
    text = lower_(tokens)
    return preStopRemoval(text)



def postBasic(tokens):
    # stripped = removeEndingPunct(tokens)
    nonDigit = [i for i in tokens if (not i.isdigit())]
    # tokens = [i for i in nonDigit if (charLength(i, 2))]
    final_tokens = [i for i in nonDigit if not i in my_stop_words]
    text = " ".join(final_tokens)

    # underScore = handleUnderScore(stripped, printDetail, True)
    return text


def mathProcessing(text, printDetail = False):
    text = HTMLParser.HTMLParser().unescape(text)   # Indexing 및 Server 실행 시
    # text = html.unescape(text)  # Request 시

    special_char_list = ['|', '=', '/', '(', ')', '[', ']', ',', '.', '_', '\'', '`', '!', '@', '#', '$', '%', '^', '&',
                         '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"', '\\']
    for s_char in special_char_list:
        text = text.replace(s_char, ' ')

    # print '1'
    tokens = getTokens(text)
    # print '2'
    # stripped = removeEndingPunct(tokens)
    # stripped = getTokens(stripped)

    # print '3'
    camelCase = handleCamelCase(tokens)

    # print '4'
    # underScore = handleUnderScore(camelCase)
    # print '5'

    lower = [i.lower() for i in camelCase]
    # print '6'
    stopped_tokens = [i for i in lower if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in my_stop_words]

    nonDigit = [i for i in stopped_tokens if (not i.isdigit())]
    tokens = [i for i in nonDigit if (charLength(i, 2))]
    final_tokens = [i for i in tokens if not i in my_stop_words]

    return " ".join(final_tokens)





















































''' No Stem for MATH project'''
def preNoStem(text, printDetail = False):
    # text = HTMLParser.HTMLParser().unescape(text) # Indexing 시

    # 기타 다른 케이스 // text = HTMLParser().unescape(text)
    text = HTMLParser().unescape(text)
    # text = html.unescape(text)

    tokens = getTokens(text)

    stripped = removeEndingPunct(tokens, printDetail)

    camelCase = handleCamelCase(stripped, printDetail, True)

    underScore = handleUnderScore(camelCase, printDetail, True)

    lower = [i.lower() for i in underScore]

    stopped_tokens = [i for i in lower if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in my_stop_words]

    nonDigit = [i for i in stopped_tokens if (not i.isdigit())]

    word = [i for i in nonDigit if (charLength(i, 2))]

    final_tokens = [i for i in word if not i in my_stop_words]

    return " ".join(final_tokens)


''' No Camel for LANG project'''
def preNoCamel(text, printDetail = False):
    special_char_list = ['=', '/', '(', ')', '[', ']', '.', '_', '\'', '`', '!', '@', '#', '$', '%', '^', '&', '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"', '\\']
    for s_char in special_char_list:
        text = text.replace(s_char, ' ')

    # Indexing 시 // text = HTMLParser.HTMLParser().unescape(text)
    # text = HTMLParser.HTMLParser().unescape(text)

    # 기타 다른 케이스 // text = HTMLParser().unescape(text)
    text = HTMLParser().unescape(text)
    # text = html.unescape(text)

    # print('Preprocessing.. #1: ', text)

    tokens = getTokens(text, printDetail)
    # print('Preprocessing.. #2: ', tokens)

    stripped = removeEndingPunct(tokens, printDetail)
    # print('Preprocessing.. #3: ', stripped)

    underScore = handleUnderScore(stripped, printDetail, True)
    # print('Preprocessing.. #4: ', underScore)

    lower = [i.lower() for i in underScore]
    # print('Preprocessing.. #5: ', lower)

    stopped_tokens = [i for i in lower if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in my_stop_words]
    # print('Preprocessing.. #6: ', stopped_tokens)

    nonDigit = [i for i in stopped_tokens if (not i.isdigit())]
    # print('Preprocessing.. #7: ', nonDigit)

    word = [i for i in nonDigit if (charLength(i, 2))]
    # print('Preprocessing.. #8: ', word)

    stem2 = stem(word, printDetail)
    final_tokens = [i for i in stem2 if not i in my_stop_words]
    # print('Preprocessing.. #9: ', final_tokens)
    return " ".join(final_tokens)


# ''' Normal from iFixR '''
# def preProcessing(text, printDetail = False):
#     text = HTMLParser.HTMLParser().unescape(text)
#     # text = html.unescape(text)
#
#     tokens = getTokens(text, printDetail)
#
#     stripped = removeEndingPunct(tokens,printDetail)
#
#     camelCase = handleCamelCase(stripped,printDetail,True)
#
#     underScore = handleUnderScore(camelCase,printDetail,True)
#
#     lower = [i.lower() for i in underScore]
#
#     stopped_tokens = [i for i in lower if not i in en_stop]
#     stopped_tokens = [i for i in stopped_tokens if not i in my_stop_words]
#
#     nonDigit = [i for i in stopped_tokens if (not i.isdigit())]
#
#     word = [i for i in nonDigit if (charLength(i,2))]
#
#     stem2 = stem(word, printDetail)
#     stem2 = [i for i in stem2 if not i in my_stop_words]
#
#     return " ".join(stem2)

if __name__ == "__main__":
    text = """2014-12-29 22:25:12,667 | ERROR | FelixStartLevel  | BlueprintCamelContext            | 8 - org.apache.camel.camel-blueprint - 2.14.0 | Error occurred during starting Camel: CamelContext(elasticSearchProducerCamelContext) due Failed to create route log-event-sink-elasticsearch at: &amp;gt;&amp;gt;&amp;gt; Aggregate[true -&amp;gt; [To[log:xxx?level=INFO&amp;amp;groupInterval=2000], To[elasticsearch://elasticsearch?ip=127.0.0.1&amp;amp;port=9300]]] &amp;lt;&amp;lt;&amp;lt; in route: Route(log-event-sink-elasticsearch)[[From[vm:log-event-elast... because of Failed to resolve endpoint: elasticsearch://elasticsearch?ip=127.0.0.1&amp;amp;port=9300 due to: Failed to resolve config path [names.txt], tried file path [names.txt], path file [xxx/config/names.txt], and classpath

org.apache.camel.FailedToCreateRouteException: Failed to create route log-event-sink-elasticsearch at: &amp;gt;&amp;gt;&amp;gt; Aggregate[true -&amp;gt; [To[log:xxx?level=INFO&amp;amp;groupInterval=2000], To[elasticsearch://elasticsearch?ip=127.0.0.1&amp;amp;port=9300]]] &amp;lt;&amp;lt;&amp;lt; in route: Route(log-event-sink-elasticsearch)[[From[vm:log-event-elast... because of Failed to resolve endpoint: elasticsearch://elasticsearch?ip=127.0.0.1&amp;amp;port=9300 due to: Failed to resolve config path [names.txt], tried file path [names.txt], path file [xxx/config/names.txt], and classpath

   at org.apache.camel.model.RouteDefinition.addRoutes(RouteDefinition.java:945)

   at org.apache.camel.model.RouteDefinition.addRoutes(RouteDefinition.java:187)

...

Caused by: org.elasticsearch.env.FailedToResolveConfigException: Failed to resolve config path [names.txt], tried file path [names.txt], path file [xxx/config/names.txt], and classpath

   at org.elasticsearch.env.Environment.resolveConfig(Environment.java:213)

   at org.elasticsearch.node.internal.InternalSettingsPreparer.prepareSettings(InternalSettingsPreparer.java:119)

...



This can be fixed by adding tmp one-liner to explicitly set the ClassLoader on the elasticSearch Settings class to the classloader of Settings.class:


            Settings settings = ImmutableSettings.settingsBuilder()

                ...

                .classLoader(Settings.class.getClassLoader());

                ..."""

    # text = '''Index(['Id', '&gt; , 'ProductId', 'UserId', 'ProfileName', 'HelpfulnessNumerator',
    #        'HelpfulnessDenominator', 'Score', 'Time', 'Summary', 'Text'],
    #       dtype='object') '=', '/', '(', ')', '[', ']', '.', '_', '`', '!', '@', '#', '$', '%', '^', '&', '*', '+', '-', '<', '>', '?', ':', ';', '{', '}', '"' '''

    '''
    Kinds
        [B] baseline
        [SPC] split by special char
        [CMC] split by camel case
        [STM] stemming
        [SWR] stop words removal 
    '''
    print(SPC(text))
    print(CMC(text))
    print(STM(text))
    print(SWR(text))
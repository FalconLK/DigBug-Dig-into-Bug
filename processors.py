#-*- coding: utf-8 -*-
# from __future__ import print_function
# import re, sys, html, os, HTMLParser    #Python2 (server)
from html.parser import HTMLParser    #Python3 (request)

import sys, re, os, html
sys.path.append(".")
sys.path.append("..")
sys.path.append("...")
sys.path.append('path_for_nltk')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from string import punctuation

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


def preBasic(text):
    # text = HTMLParser.HTMLParser().unescape(text)   # Indexing or Server
    text = html.unescape(text)    # Request
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
    nonDigit = [i for i in tokens if (not i.isdigit())]
    final_tokens = [i for i in nonDigit if not i in my_stop_words]
    text = " ".join(final_tokens)
    return text




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

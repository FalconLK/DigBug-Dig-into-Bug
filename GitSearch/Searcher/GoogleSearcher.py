#!/usr/bin/env jython
# -*- coding: utf-8 -*-

import requests, requests.utils, pickle
from os.path import join, isfile
import re, time
# import socket
# timeout = 30
# socket.setdefaulttimeout(timeout)

class YandexSearcher:
	def __init__(self, project):
		self.cookie_path = join("/tmp", ".yandex-cookie")
		self.session = None
		self.load_session()
		self.project = project

		self.project_dict = {'Hive':			'issues.apache.org/jira/browse/Hive-',
							 'Hbase':			'issues.apache.org/jira/browse/Hbase-',
							 'Camel':			'issues.apache.org/jira/browse/Camel-',
							 'Codec':			'issues.apache.org/jira/browse/Codec-',
							 'Collections':		'issues.apache.org/jira/browse/Collections-',
							 'Compress':		'issues.apache.org/jira/browse/Compress-',
							 'Configuration':	'issues.apache.org/jira/browse/Configuration-',
							 'Crypto':			'issues.apache.org/jira/browse/Crypto-',
							 'Csv':				'issues.apache.org/jira/browse/Csv-',
							 'Io':				'issues.apache.org/jira/browse/Io-',
							 'Lang':			'issues.apache.org/jira/browse/Lang-',
							 'Math':			'issues.apache.org/jira/browse/Math-',
							 'Weaver':			'issues.apache.org/jira/browse/Weaver-',
							 'Entesb':	'issues.jboss.org/browse/Entesb-',
							 'Jbmeta':	'issues.jboss.org/browse/Jbmeta-',
							 'Ely':		'issues.jboss.org/browse/Ely-',
							 'Swarm':	'issues.jboss.org/browse/Swarm-',
							 'Wfarg':	'issues.jboss.org/browse/Wfarg-',
							 'Wfcore':	'issues.jboss.org/browse/Wfcore-',
							 'Wfly':	'issues.jboss.org/browse/Wfly-',
							 'Wfmp':	'issues.jboss.org/browse/Wfmp-',

							 'Amqp':		'jira.spring.io/browse/Amqp-',
							 'Batchadm':	'jira.spring.io/browse/Batchadm-',
							 'Datajpa':		'jira.spring.io/browse/Datajpa-',
							 'Datarest':	'jira.spring.io/browse/Datarest-',
							 'Roo':			'jira.spring.io/browse/Roo-',
							 'Sgf':			'jira.spring.io/browse/Sgf-',
							 'Social':		'jira.spring.io/browse/Social-',
							 'Socialtw':	'jira.spring.io/browse/Socialtw-',
							 'Sws':			'jira.spring.io/browse/Sws-',
							 'Android':		'jira.spring.io/browse/Android-',
							 'Datacmns':	'jira.spring.io/browse/Datacmns-',
							 'Datamongo':	'jira.spring.io/browse/Datamongo-',
							 'Ldap':		'jira.spring.io/browse/Ldap-',
							 'Sec':			'jira.spring.io/browse/Sec-',
							 'Shdp':		'jira.spring.io/browse/Shdp-',
							 'Socialfb':	'jira.spring.io/browse/Socialfb-',
							 'Spr':			'jira.spring.io/browse/Spr-',
							 'Batch':		'jira.spring.io/browse/Batch-',
							 'Datagraph':	'jira.spring.io/browse/Datagraph-',
							 'Dataredis':	'jira.spring.io/browse/Dataredis-',
							 'Mobile':		'jira.spring.io/browse/Mobile-',
							 'Secoauth':	'jira.spring.io/browse/Secoauth-',
							 'Shl':			'jira.spring.io/browse/Shl-',
							 'Socialli':	'jira.spring.io/browse/Socialli-',
							 'Swf':			'jira.spring.io/browse/Swf-',
							 }
		# 'AspectJ':'https://bugs.eclipse.org/bugs/show_bug.cgi?id=' ???????
		# 'Jdt':
		# 'Pde':
		# 'Swt':
		# 'Zxing':

	def save_session(self):
		with open(self.cookie_path, 'w') as f:
			pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

	def load_session(self):
		try:
			print "Load cookie from %s" % self.cookie_path
			with open(self.cookie_path) as f:
				cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
				#print "Cookie: %s" % cookies
				self.session = requests.Session()
				self.session.cookies = cookies
		except:
			print "Created tmp cookie. Issue the request again"
			self.session = requests.Session()

	def request(self, query):
		###################### Google (구글 사용할땐, GitSearcher.py 의 search 함수에서 query 에 stackoverflow.com 넣는 부분 주석제거) ######################
		# query = {"query": query.replace(" ", "+")}
		# url = "http://www.google.com/search?hl=en&q=%(query)s&btnG=Google+Search&inurl=https" % (query)

		###################### Yandex.com ######################
		# query += ' java'
		summary = query.split('\n')[0].strip()
		summary = summary.replace(" ", "%20")
		summary = summary.replace("/", "%2F")
		summary = {"query": summary}

		description = ' '.join(query.split('\n')[1:]).strip()
		description = description.replace(" ", "%20")
		description = description.replace("/", "%2F")
		description = {"query": description}


		query = summary

		bug_report_site = self.project_dict[self.project]
		url = 'https://yandex.com/search/xml?user=falconlk&key=03.893158149:4207ac0bd65ddde2d858f4a315128d7e&query=%(query)s&lr=21204&l10n=en&site=%(bug_report_site)s' % {'query': query, 'bug_report_site': bug_report_site} #(query, self.project.upper())


		print '/////////////////////////////////////////////////////////'
		print url
		print '/////////////////////////////////////////////////////////'
		# url = 'https://yandex.com/search/xml?user=falconlk&key=03.893158149:4207ac0bd65ddde2d858f4a315128d7e&query=how+to+generate+random+string+in+java&l10n=en&sortby=tm.order%3Dascending&filter=strict&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1'

		###################### Other engines ######################
		# url = 'https://www.qwant.com/?q=%(query)s&t=web' % (query)
		# url = "http://www.bing.com/search?hl=en&q=%(query)s&btnG=Google+Search&inurl=https" % (query)
		# url = "http://www.ask.com/web?o=0&l=dir&qo=serpSearchTopBox&q=%s" % (query)

		###################### Headers ######################
		# headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36', 'accept-encoding': 'gzip;q=0,deflate,sdch'}
		headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'accept-encoding': 'gzip;q=0,deflate,sdch'}
		# headers = {
		# 	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		# 	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		# 	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		# 	'Accept-Encoding': 'none',
		# 	'Accept-Language': 'en-US,en;q=0.8',
		# 	'Connection': 'keep-alive'}


		#headers = {'User-Agent':'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'}
		#headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
		#headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0'}
		# print '\nQuery: ', query
		# print '\nURL: ', url
		# print ''
		# print 'URL: ', url
		r = self.session.get(url, headers=headers)
		# print r.text.encode("utf-8")

		# import time
		# time.sleep(1000)
		self.save_session()
		return r.text.encode("utf-8")

	def get_bug_urls(self, query):
		html = self.request(query)
		# from GitSearch.MyUtils import write_file_a
		# write_file_a('/home/ubuntu/Desktop/CoCaBu/1.html', html)
		url_list = list()
		title_list = list()
		# try:
		# 	from BeautifulSoup import BeautifulSoup
		# except ImportError:
		# 	from bs4 import BeautifulSoup
		# html = html
		# parsed_html = BeautifulSoup(html)
		# print parsed_html.body.find('div', attrs={'class': 'organic__url-text'}).text

		for url in re.findall(r'(https?://[^\s]+)', html):
			# print 'url: ', url
			# if url.startswith('https://stackoverflow.com/questions/'):

			if url.startswith('https://issues.apache.org/jira/browse/%s-' % self.project.upper()) or \
					url.startswith('https://issues.jboss.org/browse/%s-' % self.project.upper()) or \
					url.startswith('https://jira.spring.io/browse/%s-' % self.project.upper()):
				url = str(url.split('<')[0])
				url_list.append(url)
		# google 사용 시에는 위 라인들 다 지우고 아래 return 부분을 쓰면 됨.
		# return [url for url in re.findall(r'(https?://[^\s]+)', html) if url.startswith("https://stackoverflow.com/questions/")]
		return url_list

	def search(self, query):
		bug_ids = list()
		# print 'Yandex Search Query: ', query
		for idx, bug_url in enumerate(self.get_bug_urls(query)):
			# if idx > 0:	# 검색 Ranking 1위부터 10위까지 지정 부분
			# 	break
			# print 'Stackoverflow URL: ', bug_url

			bug_id = bug_url.split("/")[-1]

			if bug_id not in bug_ids:
				bug_ids.append(bug_id)
			else:
				print "Exclude", bug_id

		print "Yandex bug search ids: ", bug_ids
		return bug_ids









class GoogleSearcher:
	def __init__(self):
		# self.cookie_path = join("/tmp", ".google-cookie")
		# self.cookie_path = join("/tmp", ".bing-cookie")
		self.cookie_path = join("/tmp", ".yandex-cookie")
		self.session = None
		self.load_session()

	def save_session(self):
		with open(self.cookie_path, 'w') as f:
			pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

	def load_session(self):
		try:
			print "Load cookie from %s" % self.cookie_path
			with open(self.cookie_path) as f:
				cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
				#print "Cookie: %s" % cookies
				self.session = requests.Session()
				self.session.cookies = cookies
		except:
			print "Created tmp cookie. Issue the request again"
			self.session = requests.Session()
			
	def request(self, query):
		###################### Google (구글 사용할땐, GitSearcher.py 의 search 함수에서 query 에 stackoverflow.com 넣는 부분 주석제거) ######################
		# query = {"query": query.replace(" ", "+")}
		# url = "http://www.google.com/search?hl=en&q=%(query)s&btnG=Google+Search&inurl=https" % (query)

		###################### Yandex.com ######################
		query += ' java'
		query = {"query": query.replace(" ", "%20")}
		url = 'https://yandex.com/search/xml?user=falconlk&key=03.893158149:4207ac0bd65ddde2d858f4a315128d7e&query=%(query)s&lr=21204&l10n=en&site=stackoverflow.com' % (query)
		# url = 'https://yandex.com/search/xml?user=falconlk&key=03.893158149:4207ac0bd65ddde2d858f4a315128d7e&query=how+to+generate+random+string+in+java&l10n=en&sortby=tm.order%3Dascending&filter=strict&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1'

		###################### Other engines ######################
		# url = 'https://www.qwant.com/?q=%(query)s&t=web' % (query)
		# url = "http://www.bing.com/search?hl=en&q=%(query)s&btnG=Google+Search&inurl=https" % (query)
		# url = "http://www.ask.com/web?o=0&l=dir&qo=serpSearchTopBox&q=%s" % (query)

		###################### Headers ######################
		# headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36', 'accept-encoding': 'gzip;q=0,deflate,sdch'}
		headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'accept-encoding': 'gzip;q=0,deflate,sdch'}
		# headers = {
		# 	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		# 	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		# 	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		# 	'Accept-Encoding': 'none',
		# 	'Accept-Language': 'en-US,en;q=0.8',
		# 	'Connection': 'keep-alive'}



		#headers = {'User-Agent':'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'}
		#headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
		#headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0'}
		# print '\nQuery: ', query
		# print '\nURL: ', url
		# print ''
		r = self.session.get(url, headers=headers)
		# print r.text.encode("utf-8")

		# import time
		# time.sleep(1000)
		self.save_session()
		return r.text.encode("utf-8")

	def stackoverflow_questions(self, query):
		html = self.request(query)
		url_list = list()
		for url in re.findall(r'(https?://[^\s]+)', html):
			if url.startswith('https://stackoverflow.com/questions/'):
				url = str(url.split('<')[0])
				url_list.append(url)
		# google 사용 시에는 위 라인들 다 지우고 아래 return 부분을 쓰면 됨.
		# return [url for url in re.findall(r'(https?://[^\s]+)', html) if url.startswith("https://stackoverflow.com/questions/")]
		return url_list

	def search(self, query):
		so_ids = list()
		# print '\nGoogle Search Query: ', query
		for idx, so_url in enumerate(self.stackoverflow_questions(query)):
			# if idx > 0:	# 검색 Ranking 1위부터 10위까지 지정 부분
			# 	break
			print 'Stackoverflow URL: ', so_url

			so_id = so_url.split("/")[4]
			if so_id not in so_ids:
				so_ids.append(so_id)
			else:
				print "Exclude", so_id

		print "SO_IDs: ", so_ids
		return so_ids

class GoogleAjaxSearch:
	def search(self, query):
		query = query.replace(" ", "+")
		url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=large" % query
		print "Google Query: ", url 
		so_ids = []

		print "Before request"
		r = requests.get(url)
		print "Google JSON", r.json()
		results = r.json()["responseData"]["results"]
		for rank, res in enumerate(results[:5]):
			if res["url"].startswith("http://stackoverflow.com/questions/"):
				so_id = res["url"].split("/")[4]
				#so_ids.append({"id": so_id, "weight": len(results) - rank})


				if so_id not in []:# ["299495", "41107", "151777", "160970", "240546", "320542", "304268", "333363", "26305", "14618"]:
					so_ids.append(so_id)
				else:
					print "Excluded posts"

		print "After request"
				
		return so_ids


if __name__ == '__main__':
	from time import time
	t = time()

	q = "file encrypt"
	q += "stackoverflow java"
	google = GoogleSearcher()
	print(google.search(q))
	print(time()-t)

	t = time()
	ajax = GoogleAjaxSearch()
	print ajax.search(q)
	print(time()-t)
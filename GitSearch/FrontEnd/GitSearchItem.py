from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.token import Token
from pygments.formatters import HtmlFormatter, LatexFormatter

from utils import read_file, unescape_html

from zlib import decompress
from collections import namedtuple

import re


def generate_github_link(file_path):
	try:
		file_path_split = file_path.split("/")
		user, repo = file_path_split[6].split("_")
		rest = "/".join(file_path_split[8:])

		link = "https://github.com/%s/%s/blob/master/%s" % (user, repo, rest)
		return link

	except Exception, e:
		return "#"


class MyHtmlFormatter(HtmlFormatter):
	def __init__(self, **options):
		HtmlFormatter.__init__(self, **options)
		self.matched_terms = options["matched_terms"] if "matched_terms" in options else []
		self.matched_terms = [token.lower() for term in self.matched_terms for token in term.split(".")]

		h_terms = []
		for term in self.matched_terms:

			if "." in term:
				for token in term.split("."):
					h_terms.append(token)
			else:
				h_terms.append(term)

		self.matched_terms = h_terms



	def _my_format(self, tokensource, outfile):
		for ttype, value in tokensource:
			if value.lower() in self.matched_terms:
				yield ttype, '<span class="hll">%s</span>' % value
			# elif "." in value:
			# 	# for token in value.split(".")[:-1]:
			# 	# 	yield ttype, '<span class="hll">%s</span>' % token
			# 	# 	yield ttype, "."
			# 	# yield ttype, value.split(".")[-1]
			# 	print value
			else:
				yield ttype, value

	def format(self, tokensource, outfile):

		new_tokensource = self._my_format(tokensource, outfile) #((ttype, '<span class="hll">%s</span>' % value) if value in self.matched_terms else (ttype,value) for ttype, value in tokensource )
		HtmlFormatter.format(self, new_tokensource, outfile)

GitSearchItemSnippet = namedtuple("GitSearchItemSnippet", "html startline")
class GitSearchItem:
	def __init__(self, github_item):
		self.github_item = github_item
		self.file_path = github_item.file
		self.file_name = self.file_path.split("/")[-1]
		self.file_content = github_item.file_content
		self.code_snippets = []
		#self.file_content = decompress(github_item.code)
		self.file_content_lines = self.file_content.split("\n") if len(self.file_content.split("\n")) > 1 else self.file_content.split("\r")
		self.matched_terms = [matched_term for matched_term in github_item.matched_terms if matched_term not in ["int", "byte", "long", "short", "float", "double", "boolean", "char", "void", "String", "Integer"] and len(matched_term) > 1]
		
		self.github_link = generate_github_link(self.file_path)
		print self.github_link

		self.score = 0
		self.so_item = github_item.so_item
		print "((((((((Answer ID)))))))): ", self.so_item.answer_id
		self.so_answer_id = github_item.so_item
		self.line_numbers = self._eval(github_item.line_numbers) # allows us to map code characteristics to line numbers
		self.matching_line_numbers = [] # Lines to highlight
		#print github_item.line_numbers
		#setattr(self, "line_numbers", eval(github_item.line_numbers))
		self.html = self.highlight_code()


	def _eval(self, ln):
		# print "Before eval"
		try:
			return eval(ln)
		except:
			return {}
		# print "After eval"

		# if len(ln) > 5000:
		# 	l = dict(ln)
		# 	ln = dict(l.items()[:5000])
		# return eval(ln)

	def hl_snippet(self, source, start):

		return highlight(source, JavaLexer(), HtmlFormatter(linenos=True, anchorlinenos=True, linenostart=start))#unescape_html( highlight(source, JavaLexer(), HtmlFormatter(linenos=True, anchorlinenos=True, linenostart=start)) )

	def highlight_code(self):
		line_numbers = []
		html_snippets = []
		if self.matched_line_number():
			snippet_cluster_lns = self.compute_lines_to_highlight(self.adjacent_line_numbers())



			snippets = []
			for snippet_cluster_ln in snippet_cluster_lns:
				snippet = []

				for n in snippet_cluster_ln:
					
					snippet.append(self.file_content_lines[n])
				start_line = min(snippet_cluster_ln)
				highlight_lines = map(lambda x: x - start_line + 1, self.matching_line_numbers)
				snippets.append(("\n".join(snippet),start_line,highlight_lines))
				#self.code_snippets.append( GitSearchItemSnippet("\n".join(snippet), start_line) )

				
			# lineostart is independent from hl_lines, so we need to take care of shifting the matching line numbers
			
			#print "Highlight Lines:" + str(highlight_lines)
			#html_snippets =  ['<tmp href="%s#foo-%s">%s</tmp>' % (self.file_path, snippet[1], highlight(snippet[0], JavaLexer(), HtmlFormatter(linenos=True, anchorlinenos=True, linenostart=snippet[1]) )) for snippet in snippets] #hl_lines=snippet[2],
			html_snippets = [highlight(snippet[0], JavaLexer(), LatexFormatter(linenos=True, linenostart=snippet[1])) for snippet in snippets]
			self.code_snippets = [ GitSearchItemSnippet( self.hl_snippet( snippet[0], snippet[1]), snippet[1]) for snippet in snippets] #hl_lines=snippet[2],

		# Lexical Search does not store line number, so we are currently not able to highlight the correct location of matched term
		if not html_snippets:
			html_snippets.append(highlight(self.file_content, JavaLexer(), HtmlFormatter(linenos=True, anchorlinenos=True)))
			self.code_snippets.append( GitSearchItemSnippet( self.hl_snippet( self.file_content, 0), 0) )
				#line_numbers = list(self.matched_line_number())

		# unescape html and wrap snippets with anchor
		#html_snippets = [unescape_html(html_snippet) for html_snippet in html_snippets]

		# import uuid
		# filename = str(uuid.uuid4())
		# with open("/tmp/%s" % filename, "w") as f:
		# 	f.write("".join(html_snippets))
		#print "".join(html_snippets)


		return "".join(html_snippets)

		

	def compute_lines_to_highlight(self, ln):
		""" Returns the line number clusters of matched keywords in source file"""
		from itertools import groupby
		from operator import itemgetter


		ln = [e for e in ln if e >= 0]
		ln.sort()
		res = [map(itemgetter(1), g) for k, g in groupby(enumerate(ln), lambda (i,x):i-x)]

		return res


	# Note: is not very accurate, because we do not consider the tokens produced by lucene analyzers
	def matched_line_number(self):
		""" Returns the line number of matched keywords in source file"""
		current_line_number = 1
		matching_line_numbers = set()
		for line in self.file_content.split("\n"):
			for term in self.matched_terms:
				if term in line:
					#print "Term: %s Line: %s" % (term, line)
					matching_line_numbers.add(current_line_number)
					#print line

			current_line_number += 1

		return matching_line_numbers

	def adjacent_line_numbers(self, gap=3):
		""" Generates tmp snippet window to present the matched term(s) """
		lns = []
		for term in self.matched_terms:
			if term in self.line_numbers:
				self.matching_line_numbers.extend(self.line_numbers[term])
				for ln in self.line_numbers[term]:
					ln = self.skip_java_doc(ln)
					#print "After Java DOC line number: %s" % ln
					lns.extend(range(ln - gap, ln + gap))
					break # Test if we can avoid duplicate matches


		return list(set(lns))

	def skip_java_doc(self, ln):
		""" JDT returns start position of method declaration including its JavaDoc comment """
		if ln in self.file_content_lines:
			currentline = self.file_content_lines[ln].strip()
			max_file_lines = len(self.file_content_lines)
			while currentline.startswith(("/*", "*", "*/", "@")):
				if max_file_lines > ln:
					ln += 1
					currentline = self.file_content_lines[ln].strip()

		return ln

	def highlight_matched_terms(self, gitsearch_item_html):
		html_template = '<span class="hll">%s</span>'
		html = gitsearch_item_html
		for term in self.matched_terms:
			pattern = re.compile(r'\b%s\b' % term, re.IGNORECASE)


			#html = html.replace(term, html_template % term)
			html = pattern.sub(html_template % term, html)
			#print "term %s, replaced: %s" % (term, html_template % term)
			# Check if matched term is qualified and if it has already been something replaced
			if "." in term:
				for token in term.split("."):
					html = pattern.sub(html_template % token, html)

		return html




if __name__ == '__main__':
	path = "/Users/Raphael/Downloads/GitArchive/linkedin_indextank-engine/indextank-engine/lucene-experimental/com/flaptor/org/apache/lucene/util/automaton/UTF32ToUTF8.java"
	matched_terms = [u'Integer.toBinaryString', u'Integer']
	#i = GitSearchItem(path, matched_terms)
	file_content = read_file(path)

	print unescape_html(highlight(file_content, JavaLexer(), MyHtmlFormatter(linenos=True)))







#!/usr/bin/env python
# -*- coding: utf-8 -*-

from java.sql import Connection
from java.sql import ResultSet
from java.sql import SQLException
from java.sql import Statement
from java.sql import Date
from java.sql import Timestamp

from java.util import Calendar
from java.util import Date
from java.lang import Integer

from com.mongodb import MongoClient
from com.mongodb import DBCollection
from com.mongodb import BasicDBObject

from java.util.concurrent import Executors, TimeUnit

# from JavaCodeParser import JDTParser, parse
from NewJavaParser import parse

import utils



pool = Executors.newFixedThreadPool(4)

def convert_timestamp_to_date(timestamp):
	if timestamp:
		return Date(timestamp.getTime())
	return None

def transform_body(body):
	code_snippets = []
	code_hints = []
	for item in body.split("</code>"):
		if "<code>" in item:
			code_tag = item [item.find("<code>")+len("<code>"):]
			code_tag = utils.unescape_html(code_tag)
			if "." in code_tag and "(" in code_tag:
				code_snippets.append(code_tag)

				if "<pre" not in item and len(code_tag) < 25: # Heuristic to determine if code_tag is enclosed in inline code block
					code_hints.append(code_tag)
			elif len(code_tag) < 25:
				code_hints.append(code_tag)

	l = []
	for code_hint in code_hints:
		l.extend( utils.tokenize(code_hint) )

	code_hints = set(l)

	# parsers = [JDTParser(code_snippet, parse) for code_snippet in code_snippets]

	# futures = pool.invokeAll(parsers)

	# asts = [ future.get(3, TimeUnit.SECONDS).result for future in futures]

	#asts = [parse(code_snippet, resolve=False) for code_snippet in code_snippets]

	asts = []
	for code_snippet in code_snippets:
		ast = parse(code_snippet, resolve=True)
		if ast:
			asts.append(ast)
	

	return asts, code_hints

def parallize(doc_codes):
	parsers = [JDTParser(code, doc, parse) for doc, code in doc_codes]

	futures = pool.invokeAll(parsers)

	ast_file_docs = [ (future.get(3, TimeUnit.SECONDS).result, future.get(3, TimeUnit.SECONDS).source, future.get(3, TimeUnit.SECONDS).doc) for future in futures]

	return ast_file_docs

def createDoc(question_id, answer_id, last_edit_date, creation_date, body, score, is_accepted):
	code_snippets, code_hints = transform_body(body)
	d = {
		"question_id": question_id,
		"answer_id": answer_id,
		"last_edit_date": convert_timestamp_to_date(last_edit_date),
		"creation_date": convert_timestamp_to_date(creation_date),  		
		"is_accepted": is_accepted == 1,
		"score": score,
		"code_snippets": code_snippets,
		"code_hints": code_hints
	}

	return d




def main():
	body = """ <p>Use <tmp href="http://download.oracle.com/javase/6/docs/api/java/util/Collections.html#shuffle%28java.util.List,%20java.util.Random%29"><code>Collections.shuffle()</code></tmp> twice, with two <code>Random</code> objects initialized with the same seed:</p>  <pre><code>long seed = System.nanoTime(); Collections.shuffle(fileList, new Random(seed)); Collections.shuffle(imgList, new Random(seed)); </code></pre>  """
	body = """<p>Just use the appropriate method: <tmp href="http://docs.oracle.com/javase/8/docs/api/java/lang/String.html#split-java.lang.String-"><code>String#split()</code></tmp>.</p>

<pre><code>String string = "004-034556";
String[] parts = string.split("-");
String part1 = parts[0]; // 004
String part2 = parts[1]; // 034556
</code></pre>

<p>Note that this takes tmp <tmp href="http://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html#sum">regular expression</tmp>, so remember to escape special characters if necessary, e.g. if you want to split on period <code>.</code> which means "any character" in regex, use either <code>split("\\.")</code> or <code>split(Pattern.quote("."))</code>.</p>

<p>To test beforehand if the string contains tmp <code>-</code>, just use <tmp href="http://docs.oracle.com/javase/8/docs/api/java/lang/String.html#contains-java.lang.CharSequence-"><code>String#contains()</code></tmp>.</p>

<pre><code>if (string.contains("-")) {
    // Split it.
} else {
    throw new IllegalArgumentException("String " + string + " does not contain -");
}
</code></pre>

<p>No, this does not take tmp regular expression.</p>

"""
	body = """ <p>This is generally done with tmp simple user-defined function (i.e. Roll-your-own "isNumeric" function).</p>

<p>Something like:</p>

<pre><code>public static boolean isNumeric(String str)  
{  
  try  
  {  
    double d = Double.parseDouble(str);  
  }  
  catch(NumberFormatException nfe)  
  {  
    return false;  
  }  
  return true;  
}
</code></pre>

<p>However, if you're calling this function tmp lot, and you expect many of the checks to fail due to not being tmp number then performance of this mechanism will not be great, since you're relying upon exceptions being thrown for each failure, which is tmp fairly expensive operation.</p>

<p>An alternative approach may be to use tmp regular expression to check for validity of being tmp number:</p>

<pre><code>public static boolean isNumeric(String str)
{
  return str.matches("-?\\d+(\\.\\d+)?");  //match tmp number with optional '-' and decimal.
}
</code></pre>

<p>Be careful with the above RegEx mechanism, though, as it'll fail if your using non-latin (i.e. 0 to 9) digits.  For example, arabic digits.  This is because the "\d" part of the RegEx will only match [0-9] and effectively isn't internationally numerically aware.  (Thanks to OregonGhost for pointing this out!)</p>

<p>Or even another alternative is to use Java's built-in java.text.NumberFormat object to see if, after parsing the string the parser position is at the end of the string.  If it is, we can assume the entire string is numeric:</p>

<pre><code>public static boolean isNumeric(String str)
{
  NumberFormat formatter = NumberFormat.getInstance();
  ParsePosition pos = new ParsePosition(0);
  formatter.parse(str, pos);
  return str.length() == pos.getIndex();
}
</code></pre>
 """
	s, h = transform_body(body)

	print "----"*20
	print s
	print "----"*20
	print h



if __name__ == '__main__':
	main()
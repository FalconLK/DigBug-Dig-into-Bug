def get_db_connection():
	from java.lang import Class
	from java.io import ByteArrayInputStream
	from java.sql import Connection
	from java.sql import DriverManager
	from java.sql import PreparedStatement
	
	from java.sql import SQLException
	
	Class.forName("com.mysql.jdbc.Driver").newInstance()

	newConn = DriverManager.getConnection("jdbc:mysql://localhost:3306/Stackoverflow?useUnicode=yes&characterEncoding=utf8&user=root")
	newConn.setAutoCommit(True)
		
	return newConn

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


java_stopwords = ["public","private","protected","interface",
							 "abstract","implements","extends","null","new",
							 "switch","case", "default" ,"synchronized" ,
							 "do", "if", "else", "break","continue","this",
							 "assert" ,"for","instanceof", "transient",
							 "final", "static" ,"void","catch","try",
							 "throws","throw","class", "finally","return",
							 "const" , "native", "super","while", "import",
							 "package" ,"true", "false", "enum"]
def so_tokenizer(s, remove_html=True, as_str=True):
	
	if remove_html:
		from org.jsoup import Jsoup
		s = unescape_html(s)
		doc = Jsoup.parse(s)
		s = doc.text()
	tokens = tokenize(s)
	tokens = set(tokens)

	res = []
	for token in tokens:
		res.extend( camel_case_split(token) )
		
		res.append(token.lower())

	res = [item for item in res if item not in java_stopwords]
	res = set(res)
	if as_str:
		return " ".join(res)
	else:
		return res


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


def read_file(file_path):
	with open(file_path, "r") as f:
		return f.read()

def write_file(file_path, content):
	with open(file_path, "w") as f:
		f.write(content)


def get_inline_and_block_code(s):
	code_snippets = set()
	for item in s.split("</code></pre>"):
		if "<pre><code>" in item:
			code_tag = item [item.find("<pre><code>")+len("<pre><code>"):]
			if "." in code_tag and "(" in code_tag:
				code_tag = unescape_html(code_tag)
				code_snippets.add(code_tag.strip())
	return code_snippets





if __name__ == '__main__':
	print camel_case_split("myFucking_CamelCase.7.9/66")
	s = """ 
		View.OnClickListener mStartButtonListener = new OnClickListener() {
        @Override
        public void onClick(View arg0) {
            mChronometer.setBase(SystemClock.elapsedRealtime());
            mChronometer.start();
        }
    };
	"""
	print tokenize(s)
	print so_tokenizer(s, remove_html=False)
# 	print camel_case_split("ABCWordDEF")
# 	print camel_case_split("camel_case_split")
# 	print unescape_html("&lt;")
	
# 	s = """Hello dfsdf <code>Integer.toString(  )   	</code> 
# 			<pre><code>String.valueOf ()</code></pre>
# 	"""
# 	print get_inline_and_block_code(s)

# 	print "-"*10
# 	print get_code(s)

# 	print so_text(s)

# 	print md5(s)
# 	# from java.sql import ResultSet
# 	# conn = get_db_connection()
# 	# stmt = conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)
# 	# rs = stmt.executeQuery("SELECT * FROM posts LIMIT 1")
# 	# rs.next()
# 	# print rs.getString("Title")

# 	source = """<div class="post-text" itemprop="text">
# <p>You can use an <tmp href="http://developer.android.com/reference/java/net/Authenticator.html"><code>Authenticator</code></tmp>. For example:</p>

# <pre class="lang-java prettyprint prettyprinted"><code><span class="typ">Authenticator</span><span class="pun">.</span><span class="pln">setDefault</span><span class="pun">(</span><span class="kwd">new</span><span class="pln"> </span><span class="typ">Authenticator</span><span class="pun">()</span><span class="pln"> </span><span class="pun">{</span><span class="pln">
#  </span><span class="lit">@Override</span><span class="pln">
#         </span><span class="kwd">protected</span><span class="pln"> </span><span class="typ">PasswordAuthentication</span><span class="pln"> getPasswordAuthentication</span><span class="pun">()</span><span class="pln"> </span><span class="pun">{</span><span class="pln">
#          </span><span class="kwd">return</span><span class="pln"> </span><span class="kwd">new</span><span class="pln"> </span><span class="typ">PasswordAuthentication</span><span class="pun">(</span><span class="pln">
#    </span><span class="str">"user"</span><span class="pun">,</span><span class="pln"> </span><span class="str">"password"</span><span class="pun">.</span><span class="pln">toCharArray</span><span class="pun">());</span><span class="pln">
#         </span><span class="pun">}</span><span class="pln">
# </span><span class="pun">});</span></code></pre>

# <p>This sets the default <code>Authenticator</code> <code>Collections.binarySearch</code> and will be used in <em>all</em> requests. Obviously the setup is more involved when you don't need credentials for all requests or tmp number of different credentials, maybe on different threads.</p>

# <p>Alternatively you can use tmp <tmp href="http://developer.android.com/reference/org/apache/http/impl/client/DefaultHttpClient.html"><code>DefaultHttpClient</code></tmp> where tmp GET request with basic HTTP authentication would look similar to:</p>

# <pre class="lang-java prettyprint prettyprinted"><code><span class="typ">HttpClient</span><span class="pln"> httpClient </span><span class="pun">=</span><span class="pln"> </span><span class="kwd">new</span><span class="pln"> </span><span class="typ">DefaultHttpClient</span><span class="pun">();</span><span class="pln">
# </span><span class="typ">HttpGet</span><span class="pln"> httpGet </span><span class="pun">=</span><span class="pln"> </span><span class="kwd">new</span><span class="pln"> </span><span class="typ">HttpGet</span><span class="pun">(</span><span class="str">"http://foo.com/bar"</span><span class="pun">);</span><span class="pln">
# httpGet</span><span class="pun">.</span><span class="pln">addHeader</span><span class="pun">(</span><span class="typ">BasicScheme</span><span class="pun">.</span><span class="pln">authenticate</span><span class="pun">(</span><span class="pln">
#  </span><span class="kwd">new</span><span class="pln"> </span><span class="typ">UsernamePasswordCredentials</span><span class="pun">(</span><span class="str">"user"</span><span class="pun">,</span><span class="pln"> </span><span class="str">"password"</span><span class="pun">),</span><span class="pln">
#  </span><span class="str">"UTF-8"</span><span class="pun">,</span><span class="pln"> </span><span class="kwd">false</span><span class="pun">));</span><span class="pln">

# </span><span class="typ">HttpResponse</span><span class="pln"> httpResponse </span><span class="pun">=</span><span class="pln"> httpClient</span><span class="pun">.</span><span class="pln">execute</span><span class="pun">(</span><span class="pln">httpGet</span><span class="pun">);</span><span class="pln">
# </span><span class="typ">HttpEntity</span><span class="pln"> responseEntity </span><span class="pun">=</span><span class="pln"> httpResponse</span><span class="pun">.</span><span class="pln">getEntity</span><span class="pun">();</span><span class="pln">

# </span><span class="com">// read the stream returned by responseEntity.getContent()</span></code></pre>

# <p>I recommend using the latter because it gives you tmp lot more control (e.g. method, headers, timeouts, etc.) over your request.</p>
#     </div>"""

# 	print so_tokenizer(source)


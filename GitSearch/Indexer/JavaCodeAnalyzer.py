from java.io import StringReader

from org.apache.lucene.analysis import Analyzer
from org.apache.lucene.analysis import AnalyzerWrapper
from org.apache.lucene.analysis import TokenStream
from org.apache.lucene.analysis.Analyzer import TokenStreamComponents
from org.apache.lucene.analysis.core import TypeTokenFilter, KeywordAnalyzer
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.util import CharArraySet


class JavaCodeAnalyzer(AnalyzerWrapper):
	def __init__(self):
		self.baseAnalyzer = self.internal_analyzer()

	def internal_analyzer(self):
		java_stopwords = ["public","private","protected","interface",
							 "abstract","implements","extends","null","new",
							 "switch","case", "default" ,"synchronized" ,
							 "do", "if", "else", "break","continue","this",
							 "assert" ,"for","instanceof", "transient",
							 "final", "static" ,"void","catch","try",
							 "throws","throw","class", "finally","return",
							 "const" , "native", "super","while", "import",
							 "package" ,"true", "false", "enum"]

		all_stopwords = list(StandardAnalyzer(Version.LUCENE_CURRENT).getStopwordSet())
		all_stopwords.extend(java_stopwords)

		stopwords = CharArraySet(Version.LUCENE_CURRENT, all_stopwords, True)
		analyzer = StandardAnalyzer(Version.LUCENE_CURRENT, stopwords)
		#analyzer = KeywordAnalyzer()
		return analyzer

	def close(self):
		self.baseAnalyzer.close()
		super(JavaCodeAnalyzer, self).close()

	def getWrappedAnalyzer(self, fieldName):
		return self.baseAnalyzer

	def wrapComponents(self, fieldName, components):
		ts = components.getTokenStream()
		filteredTypes = set(["<NUM>"])
		numberFilter = TypeTokenFilter(Version.LUCENE_CURRENT, ts, filteredTypes)
		porterStem = PorterStemFilter(numberFilter)
		return TokenStreamComponents(components.getTokenizer(), porterStem)

if __name__ == '__main__':
	from utils import so_tokenizer, tokenize
	analyzer = JavaCodeAnalyzer()
	code = """ 
		View.OnClickListener mStartButtonListener = new OnClickListener() {
        @Override
        public void onClick(View arg0) {
            mChronometer.setBase(SystemClock.elapsedRealtime());
            mChronometer.start();
        }
    };
	"""

	# code = so_tokenizer(code, False)
	# print code
	ts = analyzer.tokenStream("fieldName", StringReader(code))
	ts.reset()

	while ts.incrementToken():
		ca = ts.getAttribute(CharTermAttribute)
		print ca

	analyzer.close()
		
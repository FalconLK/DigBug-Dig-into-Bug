from java.io import StringReader

from org.apache.lucene.analysis import Analyzer
from org.apache.lucene.analysis import AnalyzerWrapper
from org.apache.lucene.analysis import TokenStream
from org.apache.lucene.analysis.Analyzer import TokenStreamComponents
from org.apache.lucene.analysis.core import TypeTokenFilter
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.util import Version

from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.snowball import SnowballAnalyzer



class PorterAnalyzer(AnalyzerWrapper):
	def __init__(self, baseAnalyzer):
		self.baseAnalyzer = baseAnalyzer

	def close(self):
		self.baseAnalyzer.close()
		super(PorterAnalyzer, self).close()

	def getWrappedAnalyzer(self, fieldName):
		return self.baseAnalyzer

	def wrapComponents(self, fieldName, components):
		ts = components.getTokenStream()
		filteredTypes = set(["<NUM>"])
		numberFilter = TypeTokenFilter(Version.LUCENE_CURRENT, ts, filteredTypes)
		porterStem = PorterStemFilter(numberFilter)
		return TokenStreamComponents(components.getTokenizer(), porterStem)

if __name__ == '__main__':
	analyzer = PorterAnalyzer( StandardAnalyzer(Version.LUCENE_CURRENT))
	text = "This is tmp testing example. It should tests the Porter stemmer version 111"

	
	ts = analyzer.tokenStream("fieldName", StringReader(text))
	ts.reset()

	while ts.incrementToken():
		ca = ts.getAttribute(CharTermAttribute)
		print ca

	analyzer.close()



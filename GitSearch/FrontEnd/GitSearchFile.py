from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.token import Token
from pygments.formatters import HtmlFormatter

from utils import read_file

def highlight_file(path):
	file_content = read_file(path)
	return highlight(file_content, JavaLexer(), HtmlFormatter(linenos=True, anchorlinenos=True, lineanchors="foo") )

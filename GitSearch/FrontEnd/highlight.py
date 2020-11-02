from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.formatters import HtmlFormatter

from utils import read_file


def highlight_files(file_paths):
	highlighted_code = []
	for file_path in file_paths:
		file_content = read_file(file_path)

		code = highlight(file_content, JavaLexer(), HtmlFormatter(linenos=True))

		highlighted_code.append(code)

	return highlighted_code



class Highlight:
	def __init__(self, file_paths):
		self.file_paths = file_paths
		self.html = []
		self._process()

	def _process():
		for file_path in self.file_paths:
			file_content = read_file(file_path)

			code = highlight(file_content, JavaLexer(), HtmlFormatter(linenos=True))

			self.html.append(code)

	def highlight_code_files():
		return self.html


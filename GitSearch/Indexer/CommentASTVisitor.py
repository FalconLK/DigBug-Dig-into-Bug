from org.eclipse.jdt.core.dom import ASTVisitor, ASTNode
from org.eclipse.jdt.core.dom import MethodInvocation

class CommentASTVisitor(ASTVisitor):
	def __init__(self, cur, source):
		self.comments = []
		self.cur = cur
		self.source = source

	def get_comment(self, node):
		start = node.getStartPosition()
		end = start + node.getLength()
		comment = self.source[start:end].replace("\n", "").replace("'", "\\'").replace("\"", '\\"')
		lineNumber = self.cur.getLineNumber(node.getStartPosition()) - 1
		if comment:
			self.comments.append(comment)

	def postVisit(self, node):
		nodeType = node.getNodeType()
		if nodeType == ASTNode.LINE_COMMENT:
			self.get_comment(node)
		if nodeType == ASTNode.BLOCK_COMMENT:
			self.get_comment(node)
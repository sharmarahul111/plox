from expr import Expr

class StmtVisitor:
	def visit_print_stmt(self, expr):
		...
	def visit_expression_stmt(self, expr):
		...


class Stmt():
	def accept(self):
		pass

class Expression(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visit_expression_stmt(self)

class Print(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visit_print_stmt(self)

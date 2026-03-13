class Visitor:
	def visit_print_stmt(self, expr):
		...
	def visit_expression_stmt(self, expr):
		...


class Stmt:
	def accept(self):
		pass

class Expression(Stmt):
	def __init__(self, expr: Expr):
		self.expr = expr

	def accept(self, visitor: Visitor):
		return visitor.visit_expression_stmt()

class Print(Stmt):
	def __init__(self, expr: Expr):
		self.expr = expr

	def accept(self, visitor: Visitor):
		return visitor.visit_print_stmt()

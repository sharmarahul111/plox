"""
    Binary : Expr left, Token operator, Expr right,
    Grouping : Expr expr,
    Literal : Object value,
    Unary : Token operator, Expr right
"""
class ExprVisitor:
	def visit_binary_expr(self, expr):
		...
	def visit_grouping_expr(self, expr):
		...
	def visit_literal_expr(self, expr):
		...
	def visit_unary_expr(self, expr):
		...


class Expr:
	def accept(self):
		pass

class Binary(Expr):
	def __init__(self, left, operator: Token, right):
		self.left: Expr = left
		self.operator: Token = operator
		self.right: Right = right

	def accept(self, visitor):
		return visitor.visit_binary_expr(self)

class Grouping(Expr):
	def __init__(self, expr):
		self.expr = expr
	
	def accept(self, visitor):
		return visitor.visit_grouping_expr(self)

class Literal(Expr):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_literal_expr(self)

class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right
	def accept(self, visitor):
		return visitor.visit_unary_expr(self)
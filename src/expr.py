from Token import Token
class ExprVisitor:
	def visit_binary_expr(self, expr):
		...
	def visit_call_expr(self, expr):
		...
	def visit_get_expr(self, expr):
		...
	def visit_set_expr(self, expr):
		...
	def visit_grouping_expr(self, expr):
		...
	def visit_literal_expr(self, expr):
		...
	def visit_logical_expr(self, expr):
		...
	def visit_unary_expr(self, expr):
		...
	def visit_variable_expr(self, expr):
		...
	def visit_assign_expr(self, expr):
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

class Call(Expr):
	def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]):
		self.callee: Expr = callee
		self.paren: Token = paren
		self.arguments: list[Expr] = arguments
	
	def accept(self, visitor):
		return visitor.visit_call_expr(self)

class Get(Expr):
	def __init__(self, obj: Expr, name: Token):
		self.obj = obj
		self.name = name

	def accept(self, visitor):
		return visitor.visit_get_expr(self)

class Set(Expr):
	def __init__(self, obj: Expr, name: Token, value: Expr):
		self.obj = obj
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visit_set_expr(self)

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

class Logical(Expr):
	def __init__(self, left, operator: Token, right):
		self.left: Expr = left
		self.operator: Token = operator
		self.right: Right = right

	def accept(self, visitor):
		return visitor.visit_logical_expr(self)

class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right
	def accept(self, visitor):
		return visitor.visit_unary_expr(self)

class Variable(Expr):
	def __init__(self, name: Token):
		self.name = name
	
	def accept(self, visitor):
		return visitor.visit_variable_expr(self)

class Assign(Expr):
	def __init__(self, name: Token, value: Expr):
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visit_assign_expr(self)
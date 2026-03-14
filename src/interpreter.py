from expr import *
from stmt import *
from token_type import TokenType
from error import LoxRuntimeError
from environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):
	def __init__(self, lox):
		self.lox = lox
		self.environment = Environment()

	def interpret(self, statements: list[Stmt]):
		try:
			for statement in statements:
				self.execute(statement)
		except LoxRuntimeError as error:
			self.lox.runtime_error(error)

	def evaluate(self, expr: Expr):
		return expr.accept(self)

	def execute(self, statement: Stmt):
		return statement.accept(self)

	def execute_block(self, statements: list[Stmt], environment: Environment):
		previous = self.environment
		try:
			self.environment = environment
			for statement in statements:
				self.execute(statement)
		finally:
			self.environment = previous

	def visit_block_stmt(self, stmt: Stmt):
		self.execute_block(stmt.statements, Environment(self.environment))

	def visit_expression_stmt(self, stmt: Expression):
		self.execute(stmt.expression) # no returning

	def visit_if_stmt(self, stmt: If):
		if self.is_truthy(self.evaluate(stmt.condition)):
			self.execute(stmt.then_branch)
		elif stmt.else_branch is not None:
			self.execute(stmt.else_branch)


	def visit_print_stmt(self, stmt: Print):
		value = self.execute(stmt.expression)
		print(self.stringify(value), end='\n')

	def visit_var_stmt(self, stmt: Var):
		value = None
		if stmt.initializer is not None:
			value = self.evaluate(stmt.initializer)
		self.environment.define(stmt.name.lexeme, value)

	def visit_while_stmt(self, stmt: While):
		while self.is_truthy(self.evaluate(stmt.condition)):
			self.execute(stmt.body)

	def visit_assign_expr(self, expr: Assign):
		value = self.evaluate(expr.value)
		self.environment.assign(expr.name, value)
		return value

	def visit_binary_expr(self, expr: Binary):
		left = self.evaluate(expr.left)
		right = self.evaluate(expr.right)

		# maybe just remove those float() since already its checked
		if expr.operator.token_type == TokenType.GREATER:
			self.check_number_operands(expr.operator, left, right)
			return left > right
		elif expr.operator.token_type == TokenType.GREATER_EQUAL:
			self.check_number_operands(expr.operator, left, right)
			return left >= right
		elif expr.operator.token_type == TokenType.LESS:
			self.check_number_operands(expr.operator, left, right)
			return left < right
		elif expr.operator.token_type == TokenType.LESS_EQUAL:
			self.check_number_operands(expr.operator, left, right)
			return left <= right
		elif expr.operator.token_type == TokenType.BANG_EQUAL:
			return not self.is_equal(left, right)
		elif expr.operator.token_type == TokenType.EQUAL_EQUAL:
			return self.is_equal(left, right)
		elif expr.operator.token_type == TokenType.MINUS:
			self.check_number_operands(expr.operator, left, right)
			return left - right
		elif expr.operator.token_type == TokenType.PLUS:
			if isinstance(left, str) and isinstance(right, str):
				return left + right
			elif isinstance(left, float) and isinstance(right, float):
				return left + right
			else:
				# throw some error here for type mismatch
				raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings")
		elif expr.operator.token_type == TokenType.SLASH:
			self.check_number_operands(expr.operator, left, right)
			if right==0:
				raise LoxRuntimeError(expr.operator, "Divide by 0 not allowed")
			return left / right
		elif expr.operator.token_type == TokenType.STAR:
			self.check_number_operands(expr.operator, left, right)
			return left * right

		# Unreachable
		return None

	def visit_literal_expr(self, expr: Literal):
		return expr.value
	
	def visit_logical_expr(self, expr: Logical):
		left = self.evaluate(expr.left)
		if expr.operator.token_type == TokenType.OR:
			if self.is_truthy(left): return left
		if expr.operator.token_type == TokenType.AND:
			if not self.is_truthy(left): return left
		return self.evaluate(expr.right)

	def visit_unary_expr(self, expr: Unary):
		right = self.evaluate(expr.right)
		if expr.operator.token_type == TokenType.MINUS:
			self.check_number_operand(expr.operator, right)
			return -right
		elif expr.operator.token_type == TokenType.BANG:
			return not self.is_truthy(right)
		# Unreachable
		return None
	
	def visit_variable_expr(self, expr: Variable):
		return self.environment.get(expr.name)

	def check_number_operand(self, operator: Token, operand):
		# int would require not bool, since bool derives from int
		if isinstance(operand, float): return
		raise LoxRuntimeError(operator, "Operand must be a number")

	def check_number_operands(self, operator: Token, left, right):
		# int would require not bool, since bool derives from int
		if isinstance(left, float) and isinstance(right, float): return
		raise LoxRuntimeError(operator, "Operands must be numbers")
	

	def visit_grouping_expr(self, expr: Grouping):
		return self.evaluate(expr.expr)

	def is_truthy(self, obj) -> bool:
		if obj is None: return False
		if isinstance(obj, bool): return obj
		return True

	def is_equal(self, a, b):
		# if a is None and b is None:
		# 	return True
		# # in static languages u can't call equals() on null
		# # doesn't matter here in python i guess
		# if a is None:
		# 	return False
		return a==b

	def stringify(self, value):
		if value is None: return "nil"
		if isinstance(value, float):
			text = str(value)
			if text.endswith('.0'):
				return text[:-2]
			return text
		if isinstance(value, bool):
			return str(value).lower()
		return str(value)
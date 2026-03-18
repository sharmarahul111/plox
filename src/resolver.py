from stmt import *
from expr import *
from environment import Nil
from enum import Enum, auto

class FunctionType(Enum):
	NONE = auto()
	FUNCTION = auto()

class Resolver(StmtVisitor, ExprVisitor):
	def __init__(self, lox: Lox, interpreter: Interpreter):
		self.interpreter = interpreter
		self.scopes: list[dict] = [] #stack
		self.current_function = FunctionType.NONE
	
	def visit_block_stmt(self, stmt: Stmt):
		self.begin_scope()
		self.resolve(stmt.statements)
		self.end_scope()

	def visit_class_stmt(self, stmt: Class):
		self.declare(stmt.name)
		self.define(stmt.name)

	def visit_expression_stmt(self, stmt: Expression):
		self.resolves(stmt.expression)

	def visit_var_stmt(self, stmt: Var):
		self.declare(stmt.name)
		if stmt.initializer is not None:
			self.resolves(stmt.initializer)
		self.define(stmt.name)

	def visit_variable_expr(self, expr: Variable):
		if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
			self.lox.error(expr.name, "Can't read local variable in its own initializer.")
		self.resolve_local(expr, expr.name)

	def visit_assign_expr(self, expr: Assign):
		self.resolves(expr.value)
		self.resolve_local(expr, expr.name)

	def visit_binary_expr(self, expr: Binary):
		self.resolves(expr.left)
		self.resolves(expr.right)

	def visit_call_expr(self, expr: Call):
		self.resolves(expr.callee)
		for argument in expr.arguments:
			self.resolves(argument)

	def visit_get_expr(self, expr: Get):
		self.resolve(expr.obj)

	def visit_grouping_expr(self, expr: Grouping):
		self.resolve(expr.expr)

	def visit_literal_expr(self, expr: Literal):
		return None
	
	def visit_logical_expr(self, expr: Logical):
		self.resolves(expr.left)
		self.resolves(expr.right)

	def visit_unary_expr(self, expr: Unary):
		self.resolves(expr.right)

	def visit_function_stmt(self, stmt: Function):
		self.declare(stmt.name)
		self.define(stmt.name)
		self.resolve_function(stmt, self.current_function)

	def visit_if_stmt(self, stmt: If):
		self.resolves(stmt.condition)
		self.resolves(stmt.then_branch)
		if stmt.else_branch is not None:
			self.resolve(stmt.else_branch)

	def visit_while_stmt(self, stmt: While):
		self.resolves(stmt.condition)
		self.resolve(stmt.body)

	def visit_print_stmt(self, stmt: Print):
		self.resolves(stmt.expression)

	def visit_return_stmt(self, stmt: Return):
		if self.current_function == FunctionType.NONE:
			self.lox.error(stmt.keyword, "Can't return from top-level code.")
		if stmt.value is not None:
			self.resolves(stmt.value)

	def resolve(self, statements: list):
		for statement in statements:
			# could be either expressions or statements
			self.resolves(statement)

	def resolves(self, statement):
		statement.accept(self)

	def resolve_function(self, function: Function, function_type: FunctionType):
		enclosing_function: FunctionType = self.current_function
		self.current_function = function_type
		self.begin_scope()
		for param in function.params:
			self.declare(param)
			self.define(param)
		self.resolve(function.body)
		self.end_scope()
		self.current_function = enclosing_function

	def begin_scope(self):
		self.scopes.append({})

	def end_scope(self):
		self.scopes.pop()
	
	def declare(self, name: Token):
		if len(self.scopes) == 0:
			return
		# is only declared but not yet ready/initialized
		scope = self.scopes[-1]
		if not isinstance(scope.get(name.lexeme, Nil()), Nil):
			lox.error(name, "Already a variable with this name in this scope.")
		scope[name.lexeme] = False
	
	def define(self, name: Token):
		if len(self.scopes) == 0:
			return 0
		# is now initialized
		self.scopes[-1][name.lexeme] = True

	def resolve_local(self, expr: Expr, name: Token):
		for i in range(len(self.scopes)-1, -1, -1):
			if self.scopes[i].get(name.lexeme) is not None:
				self.interpreter.resolve(expr, len(self.scopes)-1-i)
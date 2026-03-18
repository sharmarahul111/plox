from stmt import *
from expr import *

class Resolver(StmtVisitor, ExprVisitor):
	def __init__(self, lox: Lox, interpreter: Interpreter):
		self.interpreter = interpreter
		self.scopes: list[dict] = [] #stack
	
	def visit_block_stmt(self, stmt: Stmt):
		self.begin_scope()
		self.resolve(stmt.statements)
		self.end_scope()

	def visit_var_stmt(self, stmt: Var):
		self.declare(stmt.name)
		if stmt.initializer is not None:
			self.resolve(stmt.initializer)
		self.define(stmt.name)

	def visit_variable_expr(self, expr: Variable):
		if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
			self.lox.error(expr.name, "Can't read local variable in its own initializer.")
		self.resolve_local(expr, expr.name)

	def visit_assign_expr(self, expr: Assign):
		self.resolves(expr.value)
		self.resolve_local(expr, expr.name)

	def resolve(self, statements: list):
		for statement in statements:
			# could be either expressions or statements
			self.resolves(statement)

	def resolves(self, statement):
		statement.accept(self)

	def begin_scope(self):
		self.scopes.append({})

	def end_scope(self):
		self.scopes.pop()
	
	def declare(self, name: Token):
		if len(self.scope) == 0:
			return
		# is only declared but not yet ready/initialized
		self.scopes[-1][name.lexeme] = False
	
	def define(self, name: Token):
		if len(self.scopes) == 0:
			return 0
		# is now initialized
		self.scopes[-1][name.lexeme] = True

	def resolve_local(self, expr: Expr, name: Token):
		for i in range(len(self.scopes), 0, -1):
			if self.scopes[i].get(name.lexeme) is not None:
				self.interpreter.resolve(expr, len(self.scopes)-1-i)
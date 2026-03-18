from stmt import *
from expr import *

class Resolver(StmtVisitor, ExprVisitor):
	def __init__(self, interpreter: Interpreter):
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

	def resolve(self, statements: list):
		for statement in statements:
			# could be either expressions or statements
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

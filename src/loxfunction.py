from loxcallable import LoxCallable
from environment import Environment
from expr import *
from stmt import *

class LoxFunction(LoxCallable):
	def __init__(self, declaration: Function):
		self.declaration = declaration

	def call(self, interpreter: Interpreter, arguments: list):
		environment = Environment(interpreter.globals)
		for i, param in enumerate(self.declaration.params):
			environment.define(param.lexeme, arguments[i])
		interpreter.execute_block(self.declaration.body, environment)
		# return statements later
		return None

	def arity(self):
		return len(self.declaration.params)

	def __str__(self):
		return f"<fn {self.declaration.name.lexeme}>"
from loxcallable import LoxCallable
from environment import Environment
from error import ReturnException
from expr import *
from stmt import *

class LoxFunction(LoxCallable):
	def __init__(self, declaration: Function, closure: Environment):
		self.declaration = declaration
		self.closure = closure

	def call(self, interpreter: Interpreter, arguments: list):
		environment = Environment(self.closure)
		for i, param in enumerate(self.declaration.params):
			environment.define(param.lexeme, arguments[i])
		try:
			interpreter.execute_block(self.declaration.body, environment)
		except ReturnException as return_value:
			return return_value.value
		return None
		

	def arity(self):
		return len(self.declaration.params)

	def __str__(self):
		return f"<fn {self.declaration.name.lexeme}>"
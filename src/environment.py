from Token import Token
from error import LoxRuntimeError
class Environment():
	def __init__(self, enclosing: Environment=None):
		self.values: dict = {}
		self.enclosing: Environment = enclosing

	def get(self, name: Token):
		if self.values.get(name.lexeme) is not None:
			return self.values.get(name.lexeme)
		if self.enclosing is not None:
			return self.enclosing.get(name)
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")

	def define(self, name: str, value):
		self.values[name] = value
	
	def assign(self, name: Token, value):
		if self.values.get(name.lexeme):
			self.values[name.lexeme] = value
		elif self.enclosing is not None:
			self.enclosing.assign(name, value)
		else:
			raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")
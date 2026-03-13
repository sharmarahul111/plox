from Token import Token
from error import LoxRuntimeError
class Environment():
	def __init__(self):
		self.values = {}

	def get(self, name: Token):
		if self.values.get(name.lexeme):
			return self.values.get(name.lexeme)
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")

	def define(self, name: str, value):
		self.values[name] = value
	
	def assign(self, name: Token, value):
		if self.values.get(name.lexeme):
			self.values[name.lexeme] = value
		else:
			raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")
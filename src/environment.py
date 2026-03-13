from Token import Token
from error import LoxRuntimeError
class Environment():
	def __init__(self):
		self.values = {}

	def get(self, name: Token):
		if self.values.get(name.lexeme):
			return self.values.get(name.lexeme)
		raise LoxRuntimeError(name, f"Undefined variable '{name.literal}'")


	def define(self, name: str, value):
		self.values[name] = value
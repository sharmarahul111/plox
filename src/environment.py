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

	def get_at(self, distance: int, name: str):
		return self.ancestor(distance).values[name]

	def assign_at(self, distance: int, name: Token, value):
		self.ancestor[name.lexeme] = value

	def ancestor(self, distance: int):
		environment = self
		for i in range(distance):
			environment = self.enclosing
		return environment

	def assign(self, name: Token, value):
		if self.values.get(name.lexeme) is not None:
			self.values[name.lexeme] = value
		elif self.enclosing is not None:
			self.enclosing.assign(name, value)
		else:
			raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")
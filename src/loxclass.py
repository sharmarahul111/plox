from loxcallable import LoxCallable
from Token import Token
from environment import Nil

class LoxInstance:
	def __init__(self, klass: LoxClass):
		self.klass = klass
		self.fields = {}

	def __str__(self):
		return f"{self.klass.name} instance"
	
	def get(name: Token):
		if isinstance(self.fields.get(name.lexeme, Nil()), Nil):
			return self.fields[name.lexeme]
		raise LoxRuntimeError(name, "Undefined property '" + name.lexeme + "'.")

class LoxClass(LoxCallable):
	def __init__(self, name: str):
		self.name = name

	def __str__(self):
		return f"<class {self.name}>"

	def call(self, interpreter: Interpreter, arguments: list):
		instance: LoxInstance = LoxInstance(self)
		return instance

	def arity(self):
		return 0
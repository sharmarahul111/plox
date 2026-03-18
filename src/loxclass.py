from loxcallable import LoxCallable

class LoxInstance:
	def __init__(self, klass: LoxClass):
		self.klass = klass

	def __str__(self):
		return f"{self.klass.name} instance"

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
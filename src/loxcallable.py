class LoxCallable():
	def call(self, interpreter: Interpreter, arguments: list):
		...
	def arity(self):
		...

# for easily adding builtin functions to lox
# classes may use Class or some prefix
# so for simplicity I didn't use FnClock or something like that
class LoxBuiltins:
	class Clock(LoxCallable):
		def arity(self):
			return 0;
		def call(self, interpreter: Interpreter, arguments: list):
			import time
			return time.time()
		def __str__(self):
			return '<native fn>'
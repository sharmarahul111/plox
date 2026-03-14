from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from expr import *
from token_type import TokenType
from interpreter import Interpreter
import sys
class Lox:
	def __init__(self):
		self.had_error = False
		self.had_runtime_error = False
		self.interpreter = Interpreter(self)
	def run_file(self, path: str):
		if self.had_error:
			sys.exit(65)
		if self.had_runtime_error:
			sys.exit(70)
		with open(path) as script:
			self.run(script.read())

	def run_prompt(self):
		# add a way to print expressions in REPL without ;s
		while True:
			try:
				line = input("> ")
			except (EOFError, KeyboardInterrupt):
				print()
				break
			if line.strip() == "":
				continue
			self.run(line)
			self.had_error = False

	def run(self, source):
		scanner = Scanner(self, source)
		tokens: list = scanner.scan_tokens()
		parser = Parser(self, tokens)
		statements: list[Stmt] = parser.parse()

		# stop if there was a syntax error
		if self.had_error: return
		# print(AstPrinter().prints(expr))
		self.interpreter.interpret(statements)

	def error(self, line: int, message: str) -> None:
		self.report(line, "", message)

	def report(self, line: int, where: str, message: str) -> None:
		# TODO: implement error like gcc which shows the code with formatted arrows
		print("[line", line, "] Error", where, ":", message, file=sys.stderr)
		self.had_error = True

	def parse_error(self, token: Token, message: str):
		if token.token_type == TokenType.EOF:
			self.report(token.line, "at end", message)
		else:
			self.report(token.line, f"at '{token.lexeme}'", message)

	def runtime_error(self, error):
		print(error)
		print(f"[line {error.token.line}]")
		self.had_runtime_error = True
		
	

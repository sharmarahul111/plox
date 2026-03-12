from scanner import Scanner
# import sys
class Lox:
	def __init__(self):
		self.had_error = False
	def run_file(self, path: str):
		with open(path) as script:
			self.run(script.read())

	def run_prompt(self):
		while True:
			try:
				line = input("> ")
			except (EOFError, KeyboardInterrupt):
				print()
				break
			if line.strip() == "":
				continue
			self.run(line)
			self.had_error = false

	def run(self, source):
		scanner = Scanner()
		tokens: list = scanner.scan_tokens(source)
		for token in tokens:
			print(token)
		if self.had_error:
			sys.exit(65)

	def error(self, line: int, message: str) -> None:
		report(line, "", message)

	def report(self, line: int, where: str, message: str) -> None:
		# TODO: implement error like gcc which shows the code with formatted arrows
		print("[line", line, "] Error", where, ":", message, file=sys.stderr)
		self.had_error = True
		
	

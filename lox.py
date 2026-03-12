class Lox:
	def __init__(self) :
		pass
	def run_file(self, path: str):
		with open(path) as file:
			self.run(file.read())
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
	def run(self, script):
		print("Running...")
			
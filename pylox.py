import sys
from lox import Lox


args = sys.argv[1:]
lox = Lox()
if len(args) > 1:
	print("Usage: pylox [script]")
	sys.exit(64)
elif len(args)==1:
	lox.run_file(args[0])
else:
	lox.run_prompt()
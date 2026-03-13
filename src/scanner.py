from Token import Token
from token_type import TokenType
class Scanner:
	keywords = {
		"and": TokenType.AND,
		"class": TokenType.CLASS,
		"else": TokenType.ELSE,
		"false": TokenType.FALSE,
		"for": TokenType.FOR,
		"fun": TokenType.FUN,
		"if": TokenType.IF,
		"nil": TokenType.NIL,
		"or": TokenType.OR,
		"print": TokenType.PRINT,
		"return": TokenType.RETURN,
		"super": TokenType.SUPER,
		"this": TokenType.THIS,
		"true": TokenType.TRUE,
		"var": TokenType.VAR,
		"while": TokenType.WHILE,
	}
	def __init__(self, lox, source: str):
		self.lox = lox
		self.source: str = source
		self.tokens: list[Token] = []
		self.start: int = 0
		self.current: int = 0
		self.line: int = 1
		
	def scan_tokens(self) -> list[Token]:
		while not self.is_at_end():
			self.start = self.current
			self.scan_token()

		self.tokens.append(Token(TokenType.EOF, "", None, self.line))
		return self.tokens
	
	def scan_token(self):
		# TODO: add /* comments */
		c: str = self.advance()
		if c == '(':self.add_token(TokenType.LEFT_PAREN)
		elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
		elif c == '{': self.add_token(TokenType.LEFT_BRACE)
		elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
		elif c == ',': self.add_token(TokenType.COMMA)
		elif c == '.': self.add_token(TokenType.DOT)
		elif c == '-': self.add_token(TokenType.MINUS)
		elif c == '+': self.add_token(TokenType.PLUS)
		elif c == ';': self.add_token(TokenType.SEMICOLON)
		elif c == '*': self.add_token(TokenType.STAR)
		elif c == '!':
			if self.match('='): self.add_token(TokenType.BANG_EQUAL)
			else: self.add_token(TokenType.BANG)
		elif c == '=':
			if self.match('='): self.add_token(TokenType.EQUAL_EQUAL)
			else: self.add_token(TokenType.EQUAL)
		elif c == '>':
			if self.match('='): self.add_token(TokenType.GREATER_EQUAL)
			else: self.add_token(TokenType.GREATER)
		elif c == '<':
			if self.match('='): self.add_token(TokenType.LESS_EQUAL)
			else: self.add_token(TokenType.LESS)
		elif c == '/':
			if self.match("/"):
				# // comment support
				while self.peek() != '\n' and not self.is_at_end():
					self.advance()
		
			else: self.add_token(TokenType.SLASH)
		elif c==' ' or c=='\t' or c=='\r':
			pass
		elif c=='\n': self.line+=1
		elif c=='"': self.string()
		else:
			if self.is_digit(c):
				self.number()
			elif self.is_alpha(c):
				self.identifier()
			else:
				self.lox.error(self.line, "Unexpected character")

	def match(self, expected) -> bool:
		if self.is_at_end():
			return False
		if self.source[self.current] != expected:
			return False
		self.current += 1
		return True
	def is_at_end(self) -> bool:
		return self.current >= len(self.source)

	def advance(self):
		self.current += 1
		return self.source[self.current-1]

	def peek(self):
		if self.is_at_end():
			return '\0'
		else:
			return self.source[self.current]
	def peek_next(self):
		if self.current + 1 >= len(self.source):
			return '\0'
		else:
			return self.source[self.current+1]
	def is_digit(self, c: str):
		return '0' <= c <= '9'
	def is_alpha(self, c: str):
		return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c== '_'
	def is_alphanum(self, c):
		return self.is_alpha(c) or self.is_digit(c)
	def add_token(self, token_type: TokenType, literal=None):
		text = self.source[self.start:self.current]
		self.tokens.append(Token(token_type, text, literal, self.line))

	def string(self):
		while self.peek() != '"' and not self.is_at_end():
			if self.peek() == '\n':
				self.line+=1
			self.advance()
		if self.is_at_end():
			self.lox.error(self.line, "Unterminated string")
			return
		# the closing "
		self.advance()
		# exclude surrounding quotes
		text = self.source[self.start+1:self.current-1]
		# TODO: handle escape characters here
		self.add_token(TokenType.STRING, text)

	def number(self):
		while self.is_digit(self.peek()): self.advance()
		if self.peek() == '.' and self.is_digit(self.peek_next()):
			# consume the .
			self.advance()
			while self.is_digit(self.peek()):
				self.advance()
		num = self.source[self.start:self.current]
		self.add_token(TokenType.NUMBER, float(num))
	def identifier(self):
		while(self.is_alphanum(self.peek())):
			self.advance()
		text = self.source[self.start:self.current]
		token_type = Scanner.keywords.get(text, TokenType.IDENTIFIER)
		self.add_token(token_type)
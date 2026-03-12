from token import Token
from token_type import TokenType
class Scanner:
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
		else: self.lox.error(self.line, "Unexpected Character")

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

	def add_token(self, token_type: TokenType, literal=None):
		text = self.source[self.start:self.current]
		self.tokens.append(Token(token_type, text, literal, self.line))
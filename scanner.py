from token import Token
from token_type import TokenType
class Scanner:
	def __init__(self, source: str):
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
		pass

	def is_at_end(self) -> bool:
		return self.current >= len(self.source)
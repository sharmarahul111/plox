from token import Token
from token_type import TokenType
from expr import *

class Parser:
	def __init__(self, tokens: list[Token]):
		self.tokens: list[Token] = token
		self.current = 0

	def expression(self) -> Expr:
		return self.equality()

	def equality(self) -> Expr:
		expr: Expr = self.comparison()
		while self.match(TokenType.BANG, TokenType.BANG_EQUAL):
			operator: Token = self.previous()
			right: Expr = self.comparison()
			expr = Binary(expr, operator, right)
		return expr

	def comparison(self) -> Expr:
		expr: Expr = self.term()
		while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
			operator: Token = self.previous()
			right: Expr = self.term()
			expr = Binary(expr, operator, right)
		return expr

	def term(self) -> Expr:
		expr: Expr = self.factor()
		while self.match(TokenType.PLUS, TokenType.MINUS):
			operator: Token = self.previous()
			right: Expr = self.factor()
			expr: Expr = Binary(expr, operator, right)
		return expr
	
	def factor(self) -> Expr:
		expr: Expr = self.unary()
		while self.match(TokenType.STAR, TokenType.SLASH):
			operator: Token = self.previous()
			right: Expr = self.unary()
			expr: Expr = Binary(expr, operator, right)
		return expr

	def unary(self) -> Expr:
		if self.match(TokenType.MINUS, TokenType.BANG):
			operator: Token = self.previous()
			right: Expr = self.unary()
			return Unary(operator, right)
		return self.primary()

	def primary(self):
		if self.match(TokenType.FALSE):
			return Literal(False)
		if self.match(TokenType.TRUE):
			return Literal(True)
		if self.match(TokenType.NIL):
			return Literal(None)

		if self.match(TokenType.NUMBER, TokenType.STRING):
			return Literal(self.previous().literal)

		if self.match(TokenType.LEFT_PAREN):
			expr: Expr = self.expression()
			self.consume(RIGHT_PAREN, "Expect ')' after expression.")
			return Grouping(expr)
	
	def match(self, *token_types: list[TokenType]) -> bool:
		for token_type in token_types:
			if self.check(token_type):
				advance()
				return True
		return False
	
	def consume(token_type: TokenType, message: str):
		if self.check(token_type):
			return self.advance()
		self.error(self.peek(), message)

	def check(self, token_type: TokenType) -> bool:
		if self.is_at_end(): return False
		return self.peek().token_type == token_type

	def advance(self)-> Token:
		if not self.is_at_end(): self.current+=1
		return self.previous()

	def is_at_end() -> bool:
		return self.peek().token_type == TokenType.EOF

	def peek() -> Token:
		return self.tokens[self.current]

	def previous() -> Token:
		return self.tokens[self.current - 1]

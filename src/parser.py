from Token import Token
from token_type import *
from expr import *
from stmt import *
from error import ParseError

class Parser:
	def __init__(self, lox: Lox, tokens: list[Token]):
		self.tokens: list[Token] = tokens
		self.current = 0
		self.lox = lox

	def parse(self) -> list[Stmt]:
		try:
			statements = []
			while not self.is_at_end():
				statements.append(self.declaration())
			return statements
		except ParseError as error:
			self.lox.parse_error(error.token, error)

	def expression(self) -> Expr:
		return self.assignment()

	def declaration(self) -> Stmt:
		try:
			if self.match(TokenType.FUN):
				return self.function("function")
			elif self.match(TokenType.VAR):
				return self.var_declaration()
			return self.statement()
		except ParseError as error:
			self.synchronise()
			self.lox.parse_error(error.token, error)


	def statement(self) -> Stmt:
		if self.match(TokenType.FOR):
			return self.for_statement()
		elif self.match(TokenType.IF):
			return self.if_statement()
		elif self.match(TokenType.PRINT):
			return self.print_statement()
		elif self.match(TokenType.RETURN):
			return self.return_statement()
			# add support for break and continue
		elif self.match(TokenType.WHILE):
			return self.while_statement()
		elif self.match(TokenType.LEFT_BRACE):
			return Block(self.block())
		return self.expression_statement()

	def for_statement(self):
		self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
		initializer = None
		if self.match(TokenType.SEMICOLON):
			initializer = None
		elif self.match(TokenType.VAR):
			initializer = self.var_declaration()
		else:
			initializer = self.expression_statement()

		condition: Expr = None
		if not self.check(TokenType.SEMICOLON):
			condition = self.expression()
		self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

		increment: Expr = None
		if not self.check(TokenType.RIGHT_PAREN):
			increment = self.expression()
		self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
		body: Stmt = self.statement()
		if increment is not None:
			body = Block([body, Expression(increment)])
		if condition is None:
			condition = Literal(True)
		body = While(condition, body)
		if initializer is not None:
			body = Block([initializer, body])
		return body

	def if_statement(self):
		self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
		expr: Expr = self.expression()
		self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
		then_branch: Stmt = self.statement()
		else_branch: Stmt = None
		if self.match(TokenType.ELSE):
			else_branch = self.statement()
		return If(expr, then_branch, else_branch)

	def print_statement(self):
		value: Expr = self.expression()
		self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
		return Print(value)

	def return_statement(self):
		keyword: Token = self.previous()
		value: Expr = None
		if not self.check(TokenType.SEMICOLON):
			value = self.expression()
		self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
		return Return(keyword, value)

	def var_declaration(self):
		name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
		initializer: Expr = None
		if self.match(TokenType.EQUAL):
			initializer = self.expression()
		self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
		return Var(name, initializer)

	def while_statement(self):
		self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
		condition: Expr = self.expression();
		self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
		body: Stmt = self.statement()
		return While(condition, body)

	def expression_statement(self):
		expr: Expr = self.expression()
		self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
		return Expression(expr)

	def function(self, kind: str) -> Function:
		name: Token = self.consume(TokenType.IDENTIFIER, f"Expect '{kind}' name.")
		self.consume(TokenType.LEFT_PAREN, f"Expect '(' after '{kind}' name.")
		parameters: list[Token] = []
		if not self.check(TokenType.RIGHT_PAREN):
			parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))
			while self.match(TokenType.COMMA):
				if len(parameters) >= 255:
					self.error(self.peek(), "Can't have more than 255 parameters")
					parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))
		self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
		self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
		body: list[Stmt] = self.block();
		return Function(name, parameters, body)

	def block(self):
		# assumes the '{' token has already been matched
		statements = []
		while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
			statements.append(self.declaration())
		self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
		return statements

	def assignment(self):
		expr: Expr = self.logical_or()
		if self.match(TokenType.EQUAL):
			equals: Token = self.previous()
			value: Expr = self.assignment()
			if isinstance(expr, Variable):
				name: Token = expr.name
				return Assign(name, value)
			self.error(equals, "Invalig assignment target.")
		return expr

	def logical_or(self):
		expr: Expr = self.logical_and()
		while self.match(TokenType.OR):
			operator: Token = self.previous()
			right: Expr = self.logical_and()
			expr = Logical(expr, operator, right)
		return expr

	def logical_and(self):
		expr: Expr = self.equality()
		while self.match(TokenType.AND):
			operator: Token = self.previous()
			right: Expr = self.equality()
			expr = Logical(expr, operator, right)
		return expr

	def equality(self) -> Expr:
		expr: Expr = self.comparison()
		while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
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
		return self.call()
	
	def finish_call(self, callee: Expr):
		arguments = []
		if not self.check(TokenType.RIGHT_PAREN):
			arguments.append(self.expression())
			while self.match(TokenType.COMMA):
				if len(arguments) >= 255:
					self.error(self.peek(), "Can't have more than 255 arguments.")
				arguments.append(self.expression)
		paren: Token = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
		return Call(callee, paren, arguments)

	def call(self) -> Expr:
		expr: Expr = self.primary()
		while True:
			if self.match(TokenType.LEFT_PAREN):
				expr = self.finish_call(expr)
			else:
				break
		return expr

	def primary(self):
		if self.match(TokenType.FALSE):
			return Literal(False)
		if self.match(TokenType.TRUE):
			return Literal(True)
		if self.match(TokenType.NIL):
			return Literal(None)

		if self.match(TokenType.NUMBER, TokenType.STRING):
			return Literal(self.previous().literal)
		if self.match(TokenType.IDENTIFIER):
			return Variable(self.previous())

		if self.match(TokenType.LEFT_PAREN):
			expr: Expr = self.expression()
			self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
			return Grouping(expr)
		raise self.error(self.peek(), "Expect expression")

	def match(self, *token_types: TokenType) -> bool:
		for token_type in token_types:
			if self.check(token_type):
				self.advance()
				return True
		return False
	
	def consume(self, token_type: TokenType, message: str):
		if self.check(token_type):
			return self.advance()
		self.error(self.peek(), message)

	def error(self, token: Token, message: str):
		raise ParseError(token, message)

	def synchronise(self):
		self.advance()
		while not self.is_at_end():
			if self.previous().token_type == TokenType.SEMICOLON: return
			if self.peek().token_type in [TokenType.CLASS, TokenType.VAR, TokenType.IF, TokenType.FOR, TokenType.FUN,
			TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]:
				return
			self.advance()

	def check(self, token_type: TokenType) -> bool:
		if self.is_at_end():
			return False
		return self.peek().token_type == token_type

	def advance(self)-> Token:
		if not self.is_at_end(): self.current+=1
		return self.previous()

	def is_at_end(self) -> bool:
		return self.peek().token_type == TokenType.EOF

	def peek(self) -> Token:
		return self.tokens[self.current]

	def previous(self) -> Token:
		return self.tokens[self.current - 1]

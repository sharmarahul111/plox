from expr import *

class AstPrinter(Visitor):
	def prints(self, expr):
		return expr.accept(self)
	
	def visit_binary_expr(self, expr: Binary):
		return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
	
	def visit_grouping_expr(self, expr: Grouping):
		return self.parenthesize("group", expr.expr)

	def visit_literal_expr(self, expr: Literal):
		if expr.value == None: return "nil";
		return str(expr.value);

	def visit_unary_expr(self, expr: Unary):
		return self.parenthesize(expr.operator.lexeme, expr.right)

	def parenthesize(self, name, *exprs):
		parts = [name]+[expr.accept(self) for expr in exprs]
		return f"({' '.join(parts)})"

if __name__ == "__main__":
	from Token import Token
	from token_type import TokenType
	expr = Binary(
		Unary(
			Token(TokenType.MINUS, "-", None, 1),
			Literal(123)
		),
		Token(TokenType.STAR, "*", None, 1),
		Grouping(
            Literal(45.67)
		)
	)

	print(AstPrinter().prints(expr))
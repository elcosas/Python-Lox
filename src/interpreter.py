from expressions import *
from statements import *
from visitor import Visitor
from enviornment import Enviornment
from token_type import TokenType
from error import error, RuntimeErr

class Interpreter(Visitor):
    environ: Enviornment = Enviornment()

    def interpret(self, stmts: list[Stmt]) -> None:
        try:
            for stmt in stmts:
                stmt.accept(self)
        except RuntimeErr as err:
            error(line=err.token.line, token=err.token, msg=err.message)
            return None

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return expr.expression.accept(self)

    def visit_unary_expr(self, expr: Unary) -> object:
        right: object = expr.right.accept(self)
        if expr.operator.type == TokenType.MINUS:
            self.check_operands(right)
            return -float(right)
        return None

    def visit_variable_expr(self, expr: Variable) -> object:
        return self.environ.get(expr.name)

    def visit_assign_expr(self, expr: Assign) -> object:
        value: object = expr.value.accept(self)
        self.environ.assign(expr.name, value)
        return value

    def visit_binary_expr(self, expr: Binary) -> object:
        left: object = expr.left.accept(self)
        right: object = expr.right.accept(self)
        if expr.operator.type == TokenType.MINUS:
            self.check_operands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.type == TokenType.SLASH:
            self.check_operands(expr.operator, left, right)
            if float(right) == 0.0:
                raise RuntimeErr(expr.operator, 'Can\'t divide by zero.')
            return float(left) / float(right)
        if expr.operator.type == TokenType.STAR:
            self.check_operands(expr.operator, left, right)
            return float(left) * float(right)
        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right) 
            raise RuntimeErr(expr.operator, 'Operands must be two numbers or two strings.')
        return None
    
    def visit_expression_stmt(self, stmt: Expression) -> None:
        stmt.expression.accept(self)
    
    def visit_print_stmt(self, stmt: Print) -> None:
        value: object = stmt.expression.accept(self)
        print(self.stringify(value))
    
    def visit_var_stmt(self, stmt: Var) -> None:
        value: object = None
        if stmt.initializer is not None:
            value = stmt.initializer.accept(self)
        self.environ.define(stmt.name.lexeme, value)

    # Utilities
    def check_operands(self, operator: Token, *operands: list[object]) -> None:
        for operand in operands:
            if not isinstance(operand, float):
                raise RuntimeErr(operator, 'Operand must be a number.')
    
    def stringify(self, obj: object) -> str:
        if obj is None:
            return 'none'
        if isinstance(obj, float):
            text: str = str(obj)
            if text.endswith('.0'):
                return text[:len(text)-2]
            return text
        return str(obj)
from expressions import *
from statements import *
from visitor import Visitor
from environment import Environment
from token_type import TokenType
from error import error, RuntimeErr

class Interpreter(Visitor):
    def __init__(self):
        self.environ: Environment = Environment()

    def interpret(self, stmts: list[Stmt]) -> None:
        try:
            for stmt in stmts:
                stmt.accept(self)
        except RuntimeErr as err:
            error(line=err.token.line, token=err.token, msg=err.message)
            return None

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    def visit_logical_expr(self, expr: Logical) -> object:
        left: object = expr.left.accept(self)
        if (expr.operator.type == TokenType.OR):
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return expr.right.accept(self)

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return expr.expression.accept(self)

    def visit_unary_expr(self, expr: Unary) -> object:
        right: object = expr.right.accept(self)
        if expr.operator.type == TokenType.MINUS:
            self.check_operands(right)
            return -float(right)
        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
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
        if expr.operator.type == TokenType.GREATER:
            self.check_operands(expr.operator, left, right)
            return float(left) > float(right)
        if expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if expr.operator.type == TokenType.LESS:
            self.check_operands(expr.operator, left, right)
            return float(left) < float(right)
        if expr.operator.type == TokenType.LESS_EQUAL:
            self.check_operands(expr.operator, left, right)
            return float(left) <= float(right)
        if expr.operator.type == TokenType.MINUS:
            self.check_operands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
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

    def visit_if_stmt(self, stmt: If) -> None:
        if self.is_truthy(stmt.condition.accept(self)):
            stmt.then_branch.accept(self)
        elif stmt.else_branch is not None:
            stmt.else_branch.accept(self)
        return None
    
    def visit_print_stmt(self, stmt: Print) -> None:
        value: object = stmt.expression.accept(self)
        print(self.stringify(value))
    
    def visit_var_stmt(self, stmt: Var) -> None:
        value: object = None
        if stmt.initializer is not None:
            value = stmt.initializer.accept(self)
        self.environ.define(stmt.name.lexeme, value)

    def visit_while_stmt(self, stmt: While) -> None:
        while self.is_truthy(stmt.condition.accept(self)):
            stmt.body.accept(self)
        return None
     
    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environ))
        return None

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous: Environment = self.environ
        try:
            self.environ = environment
            for stmt in statements:
                stmt.accept(self)
        finally:
            self.environ = previous

    # Utilities
    def is_truthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def is_equal(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

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

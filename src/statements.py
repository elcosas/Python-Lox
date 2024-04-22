from abc import ABC, abstractmethod
from token_cls import Token
from expressions import Expr

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression
    
    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression
    
    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

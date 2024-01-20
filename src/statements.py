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
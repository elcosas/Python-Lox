from abc import ABC, abstractmethod
from expressions import *
from statements import *

class Visitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: Assign) -> object:
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> object:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> object:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> object:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> object:
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: Variable) -> object:
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression) -> None:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Print) -> None:
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: Var) -> None:
        pass

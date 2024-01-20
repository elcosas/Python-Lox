from expressions import *
from statements import *
from token_cls import Token
from token_type import TokenType
from error import ParseErr

class Parser:
    cur: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
    
    def parse(self) -> list[Stmt]:
        stmts: list[Stmt] = []
        while not self.tok_end():
            stmts.append(self.declaration())
        return stmts
    
    # Rule expansions
    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseErr:
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, 'Expected variable name.')
        initializer: Expr = None
        if self.match(TokenType.EQUAl):
            initializer = self.expression()
        self.consume(TokenType.SEMICOlON, 'Expected \';\' after variable declaration.')
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOlON, 'Expected \';\' after value.')
        return Print(value)
    
    def expression_statement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOlON, 'Expected \';\' after expression.')
        return Expression(expr)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr: Expr = self.term()
        if self.match(TokenType.EQUAl):
            equals: Token = self.previous()
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            raise ParseErr(equals, 'Invalid assignment target.')
        return expr
    
    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            oper: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, oper, right)
        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            oper: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, oper, right)
        return expr
    
    def unary(self) -> Expr:
        if self.match(TokenType.MINUS):
            oper: Token = self.previous()
            right: Expr = self.unary()
            return Unary(oper, right)
        return self.primary()
    
    def primary(self) -> Expr:
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'Expect \')\' after expression.')
            return Grouping(expr)
        
        raise ParseErr(self.peek(), 'Expect expression.')
    
    # Helper functions
    def match(self, *types: TokenType) -> bool:
        for ttype in types:
            if self.check(ttype):
                self.advance()
                return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> object:
        if self.check(token_type):
            return self.advance()
        raise ParseErr(self.peek(), message)
    
    def synchronize(self) -> None:
        self.advance()
        while not self.tok_end():
            ttype: TokenType = self.peek().type
            if ttype == TokenType.PRINT or ttype == TokenType.VAR:
                return
            self.advance()
    
    def check(self, ttype: TokenType) -> bool:
        if self.tok_end():
            return False
        return self.peek().type == ttype
    
    def advance(self) -> Token:
        if not self.tok_end():
            self.cur += 1
        return self.previous()
    
    def tok_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.cur]
    
    def previous(self) -> Token:
        return self.tokens[self.cur - 1]

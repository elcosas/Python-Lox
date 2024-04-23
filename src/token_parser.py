from expressions import *
from statements import *
from token_cls import Token
from token_type import TokenType
from error import ParseErr

class Parser:
    cur: int = 0

    synch_toks = [
        TokenType.CLASS,
        TokenType.FUN,
        TokenType.VAR,
        TokenType.FOR,
        TokenType.IF,
        TokenType.WHILE,
        TokenType.PRINT,
        TokenType.RETURN
    ]

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
    
    def parse(self) -> list[Stmt]:
        stmts: list[Stmt] = []
        while not self.tok_end():
            stmts.append(self.declaration())
        return stmts
    
    # rule expansions
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
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, 'Expected \';\' after variable declaration.')
        return Var(name, initializer)

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, 'Expected \'(\' after \'while\'.')
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'Expected \')\' after condition.')
        body: Stmt = self.statement()
        return While(condition, body)

    def statement(self) -> Stmt:
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, 'Expected \'(\' after \'if\'.')
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'Expected \')\' after if condition.')
        then_branch: Stmt = self.statement()
        else_branch: Stmt = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return If(condition, then_branch, else_branch)

    def print_statement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, 'Expected \';\' after value.')
        return Print(value)
    
    def expression_statement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, 'Expected \';\' after expression.')
        return Expression(expr)

    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.tok_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, 'Expected \'}\' after block.')
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr: Expr = self.or_op()
        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            raise ParseErr(equals, 'Invalid assignment target.')
        return expr
    
    def or_op(self) -> Expr:
        expr: Expr = self.and_op()
        while self.match(TokenType.OR):
            operator: Token = self.previous()
            right: Expr = self.and_op()
            expr = Logical(expr, operator, right)
        return expr

    def and_op(self) -> Expr:
        expr: Expr = self.equality()
        while self.match(TokenType.AND):
            operator: Token = self.previous()
            right: Expr = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            oper: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, oper, right)
        return expr
    
    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            oper: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, oper, right)
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
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.MODULO):
            oper: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, oper, right)
        return expr
    
    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            oper: Token = self.previous()
            right: Expr = self.unary()
            return Unary(oper, right)
        return self.primary()
    
    def primary(self) -> Expr:
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
            if ttype in self.synch_toks:
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

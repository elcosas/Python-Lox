from token_cls import Token
from token_type import TokenType
from error import error

class Scanner:
    keywords: dict[str, TokenType] = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE
    }

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
    
    def scan_tokens(self) -> list[Token]:
        while not self.current >= len(self.source):
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line));
        return self.tokens

    def scan_token(self) -> None:
        char: str = self.source[self.current]
        self.current += 1
        if char == ' ' or char == '\r' or char == '\t':
            pass
        elif char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '.':
            self.add_token(TokenType.DOT)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == ';':
            self.add_token(TokenType.SEMICOlON)
        elif char == '*':
            self.add_token(TokenType.STAR)
        elif char == '!':
            self.add_token(TokenType.BANG_EQUAL if self.char_match('=') else TokenType.BANG)
        elif char == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.char_match('=') else TokenType.EQUAL)
        elif char == '<':
            self.add_token(TokenType.LESS_EQUAL if self.char_match('=') else TokenType.LESS)
        elif char == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.char_match('=') else TokenType.GREATER)
        elif char == '/':
            if self.char_match('/'):
                while self.peek() != '\n' and not self.current >= len(self.source):
                    self.current += 1
            elif self.char_match('*'):
                while not self.current >= len(self.source):
                    if self.peek() == '*':
                        if self.peek_next() == '/':
                            break
                    if self.source[self.current] == '\n':
                        self.line += 1
                    self.current += 1
                self.current += 2
            else:
                self.add_token(TokenType.SLASH)
        elif char == '"':
            self.scan_string()
        elif char == '\n':
            self.line += 1
        else:
            if char.isdigit():
                self.scan_number()
            elif char.isalpha():
                self.scan_identifier()
            else:
                error(line=self.line, msg='Unexpected Character.')

    def scan_string(self) -> None:
        while self.peek() != '"' and not self.current >= len(self.source):
            if self.peek() == '\n':
                self.line += 1
            self.current += 1

        if self.current >= len(self.source):
            error(line=self.line, msg='Unterminated String.')
            return
            
        self.current += 1
        value: str = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, literal=value)

    def scan_number(self) -> None:
        while self.peek().isdigit(): 
            self.current += 1
        if self.peek() == '.' and self.peek_next().isdigit():
            self.current += 1
            while self.peek().isdigit():
                self.current += 1
        self.add_token(TokenType.NUMBER, literal=float(self.source[self.start:self.current]))

    def scan_identifier(self) -> None:
        while self.peek().isalnum():
            self.current += 1
        text: str = self.source[self.start:self.current]
        try:
            token_type: TokenType = self.keywords[text]
        except KeyError:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)

    def char_match(self, expected: str) -> bool:
        if self.current >= len(self.source):
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.current >= len(self.source):
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if (self.current + 1) >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType, literal: object=None) -> None:
        token: str = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, token, literal, self.line))

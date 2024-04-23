from enum import Enum

class TokenType(Enum):
    # single char tokens
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    MODULO = 12

    # 1-2 char tokens
    BANG = 13
    BANG_EQUAL = 14
    EQUAL = 15
    EQUAL_EQUAL = 16
    GREATER = 17
    GREATER_EQUAL = 18
    LESS = 19
    LESS_EQUAL = 20
    
    # literals
    IDENTIFIER = 21
    STRING = 22
    NUMBER = 23

    # Keywords
    AND = 24
    CLASS = 25
    ELSE = 26
    FALSE = 27
    FUN = 28
    FOR = 29
    IF = 30
    NIL = 31
    OR = 32
    PRINT = 33
    RETURN = 34
    SUPER = 35
    THIS = 36
    TRUE = 37
    VAR = 38
    WHILE = 39
    EOF = 40

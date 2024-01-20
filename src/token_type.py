from enum import Enum

class TokenType(Enum):
    # Keywords
    VAR = 1
    PRINT = 2
    EOF = 3

    # Operators
    EQUAl = 4
    MINUS = 5
    PLUS = 6
    SLASH = 7
    STAR = 8

    # Types
    STRING = 9
    NUMBER = 10
    IDENTIFIER = 11

    # Grouping
    LEFT_PAREN = 12
    RIGHT_PAREN = 13
    SEMICOlON = 14

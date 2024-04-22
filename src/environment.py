from error import error
from token_cls import Token

class Environment:
    def __init__(self, enclosing: object=None) -> None:
        self.values: dict[str, object] = {}
        if enclosing is not None:
            self.enclosing = enclosing
        else:
            self.enclosing: object = None

    def define(self, name: str, value: object) -> None:
        self.values.update({name: value})
    
    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        error(line=name.line, token=name, msg=f'Undefined variable \'{name.lexeme}\'.')

    def get(self, name: Token) -> object:
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        error(line=name.line, token=name, msg=f'Undefined variable \'{name.lexeme}\'.')

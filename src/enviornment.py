from error import error
from token_cls import Token

class Enviornment:
    values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self.values.update({name: value})
    
    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        error(line=name.line, token=name, msg=f'Undefined variable \'{name.lexeme}\'.')

    def get(self, name: Token) -> object:
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        error(line=name.line, token=name, msg=f'Undefined variable \'{name.lexeme}\'.')
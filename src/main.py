#!/usr/bin/env python3

from sys import argv, exit
from error import get_err_status, set_err_status
from token_cls import Token
from statements import Stmt
from scanner import Scanner
from token_parser import Parser
from interpreter import Interpreter

def main() -> None:
    if len(argv) > 2:
        raise Exception("Usage: jlox [script]")
    elif len(argv) == 2:
        run_script(argv[1])
    else:
        run_prompt()

def run_script(path: str) -> None:
    with open(path, 'r') as f:
        text: list[str] = ''.join(f.readlines())
    run(text)
    if get_err_status():
        exit(1)
    exit(0)

def run_prompt() -> None:
    print(version_info())
    is_running: bool = True
    while is_running:
        try:
            text: str = input('>> ')
            if text == '':
                raise EOFError
            else:
                run(text)
                set_err_status(False)
        except (KeyboardInterrupt, EOFError):
            print('')
            is_running = False
    exit(0)

def version_info() -> None:
    print('Welcome to python-lox 1.0!')

def run(source: str) -> None:
    scanner: Scanner = Scanner(source)
    tokens: list[Token] = scanner.scan_tokens()
    parser: Parser = Parser(tokens)
    statements: list[Stmt] = parser.parse()
    if get_err_status():
        return
    interpreter: Interpreter = Interpreter()
    interpreter.interpret(statements)

if __name__ == '__main__':
    main()

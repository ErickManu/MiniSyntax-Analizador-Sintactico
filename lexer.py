"""Convierte el texto MiniSyntax en tokens con línea y columna."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    line: int
    column: int


class LexerError(Exception):
    def __init__(self, line, column, found, expected, description):
        self.line = line
        self.column = column
        self.found = found
        self.expected = expected
        super().__init__(
            f"Error léxico en línea {line}, columna {column}:\n"
            f"{description}\nEncontrado: {found!r}\nEsperado: {expected}"
        )


class Lexer:
    KEYWORDS = {
        "int": "TYPE", "float": "TYPE", "string": "TYPE", "bool": "TYPE",
        "true": "BOOLEAN", "false": "BOOLEAN", "if": "IF", "else": "ELSE",
        "while": "WHILE", "print": "PRINT",
    }
    DOUBLE = {
        "==": "EQUAL", "!=": "NOT_EQUAL", ">=": "GREATER_EQUAL",
        "<=": "LESS_EQUAL", "&&": "AND", "||": "OR",
    }
    SINGLE = {
        "+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE",
        "%": "MODULO", "=": "ASSIGN", ">": "GREATER", "<": "LESS",
        "!": "NOT", "(": "LPAREN", ")": "RPAREN", "{": "LBRACE",
        "}": "RBRACE", ";": "SEMICOLON",
    }

    def __init__(self, source):
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        self.position = 0
        self.line = 1
        self.column = 1

    def advance(self):
        char = self.source[self.position]
        self.position += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    @staticmethod
    def is_letter(char):
        return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"

    @staticmethod
    def is_digit(char):
        return "0" <= char <= "9"

    def tokenize(self):
        tokens = []
        while self.position < len(self.source):
            char = self.source[self.position]
            if char.isspace():
                self.advance()
                continue

            start, line, column = self.position, self.line, self.column
            if self.is_letter(char):
                self.advance()
                while self.position < len(self.source):
                    char = self.source[self.position]
                    if not (self.is_letter(char) or self.is_digit(char)):
                        break
                    self.advance()
                value = self.source[start:self.position]
                kind = self.KEYWORDS.get(value, "IDENTIFIER")
            elif self.is_digit(char):
                while self.position < len(self.source) and self.is_digit(self.source[self.position]):
                    self.advance()
                if self.position < len(self.source) and self.source[self.position] == ".":
                    self.advance()
                    if self.position == len(self.source) or not self.is_digit(self.source[self.position]):
                        raise LexerError(line, column, self.source[start:self.position],
                                         "un decimal como 85.5", "Faltan dígitos después del punto.")
                    while self.position < len(self.source) and self.is_digit(self.source[self.position]):
                        self.advance()
                value, kind = self.source[start:self.position], "NUMBER"
            elif char == '"':
                self.advance()
                while True:
                    if self.position == len(self.source) or self.source[self.position] == "\n":
                        raise LexerError(line, column, self.source[start:self.position],
                                         'comilla de cierre (\")', "La cadena no está cerrada en la misma línea.")
                    char = self.advance()
                    if char == '"':
                        break
                    if char == "\\":
                        if self.position == len(self.source) or self.source[self.position] not in '\\"ntr':
                            raise LexerError(self.line, self.column, self.source[self.position:self.position + 1],
                                             r'\", \\, \n, \t o \r', "Secuencia de escape no válida.")
                        self.advance()
                value, kind = self.source[start:self.position], "STRING"
            else:
                pair = self.source[self.position:self.position + 2]
                if pair in self.DOUBLE:
                    value, kind = pair, self.DOUBLE[pair]
                    self.advance()
                    self.advance()
                elif char in self.SINGLE:
                    value, kind = char, self.SINGLE[char]
                    self.advance()
                else:
                    raise LexerError(line, column, char, "un símbolo del lenguaje MiniSyntax",
                                     "Carácter no reconocido.")
            tokens.append(Token(kind, value, line, column))
        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens

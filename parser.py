"""Parser descendente recursivo: valida estructura, sin ejecutar el código."""


class ParserError(Exception):
    def __init__(self, token, expected, description, line=None):
        self.line = token.line if line is None else line
        self.column = token.column
        self.token = token
        self.expected = expected
        found = "fin del código (EOF)" if token.type == "EOF" else f"{token.value!r} ({token.type})"
        location = f"línea {self.line}"
        if token.type != "EOF":
            location += f", columna {self.column}"
        super().__init__(
            f"Error sintáctico en {location}:\n{description}\n"
            f"Encontrado: {found}\nEsperado: {expected}"
        )


class Parser:
    def __init__(self, tokens):
        if not tokens or tokens[-1].type != "EOF":
            raise ValueError("La lista de tokens debe terminar con EOF.")
        self.tokens = tokens
        self.position = 0

    @property
    def current(self):
        return self.tokens[self.position]

    def match(self, *types):
        if self.current.type in types:
            self.position += 1
            return True
        return False

    def error(self, expected, description):
        # En EOF, señalar la última línea de código facilita ubicar el faltante.
        line = None
        if self.current.type == "EOF" and self.position:
            line = self.tokens[self.position - 1].line
        raise ParserError(self.current, expected, description, line)

    def expect(self, kind, expected, description):
        if not self.match(kind):
            self.error(expected, description)

    def parse(self):
        while self.current.type != "EOF":
            self.statement()
        return True

    def statement(self):
        kind = self.current.type
        if kind == "TYPE":
            self.declaration()
        elif kind == "IDENTIFIER":
            self.assignment()
        elif kind == "PRINT":
            self.print_statement()
        elif kind == "IF":
            self.conditional()
        elif kind == "WHILE":
            self.while_statement()
        else:
            self.error("tipo, identificador, print, if o while", "Se esperaba el inicio de una sentencia.")

    def declaration(self):
        self.position += 1
        self.expect("IDENTIFIER", "un identificador", "Se esperaba un identificador después del tipo.")
        if self.match("ASSIGN"):
            self.expression()
        self.expect("SEMICOLON", "';'", "Se esperaba ';' después de la declaración.")

    def assignment(self):
        self.position += 1
        self.expect("ASSIGN", "'='", "Se esperaba '=' después del identificador.")
        self.expression()
        self.expect("SEMICOLON", "';'", "Se esperaba ';' después de la asignación.")

    def print_statement(self):
        self.position += 1
        self.expect("LPAREN", "'('", "Se esperaba '(' después de print.")
        self.expression()
        self.expect("RPAREN", "')'", "Se esperaba ')' para cerrar print.")
        self.expect("SEMICOLON", "';'", "Se esperaba ';' después de print.")

    def conditional(self):
        self.position += 1
        self.expect("LPAREN", "'('", "Se esperaba '(' después de if.")
        self.expression()
        self.expect("RPAREN", "')'", "Se esperaba ')' después de la condición de if.")
        self.block()
        if self.match("ELSE"):
            self.block()

    def while_statement(self):
        self.position += 1
        self.expect("LPAREN", "'('", "Se esperaba '(' después de while.")
        self.expression()
        self.expect("RPAREN", "')'", "Se esperaba ')' después de la condición de while.")
        self.block()

    def block(self):
        self.expect("LBRACE", "'{'", "Se esperaba '{' para iniciar el bloque.")
        while self.current.type not in ("RBRACE", "EOF"):
            self.statement()
        self.expect("RBRACE", "'}'", "Se esperaba '}' para cerrar el bloque.")

    # Cada nivel llama al siguiente, que tiene mayor precedencia.
    def expression(self):
        self.logical_or()

    def logical_or(self):
        self.logical_and()
        while self.match("OR"):
            self.logical_and()

    def logical_and(self):
        self.equality()
        while self.match("AND"):
            self.equality()

    def equality(self):
        self.comparison()
        while self.match("EQUAL", "NOT_EQUAL"):
            self.comparison()

    def comparison(self):
        self.term()
        while self.match("GREATER", "LESS", "GREATER_EQUAL", "LESS_EQUAL"):
            self.term()

    def term(self):
        self.factor()
        while self.match("PLUS", "MINUS"):
            self.factor()

    def factor(self):
        self.unary()
        while self.match("MULTIPLY", "DIVIDE", "MODULO"):
            self.unary()

    def unary(self):
        if self.match("NOT", "PLUS", "MINUS"):
            self.unary()
        else:
            self.primary()

    def primary(self):
        if self.match("NUMBER", "STRING", "BOOLEAN", "IDENTIFIER"):
            return
        if self.match("LPAREN"):
            self.expression()
            self.expect("RPAREN", "')'", "Se esperaba ')' para cerrar la expresión.")
            return
        self.error("número, cadena, booleano, identificador o '('", "Se esperaba una expresión o un operando.")

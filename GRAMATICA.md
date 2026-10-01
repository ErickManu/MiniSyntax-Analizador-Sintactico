# Gramática de MiniSyntax

MiniSyntax es un lenguaje educativo para demostrar análisis léxico y sintáctico. Describe declaraciones, asignaciones, impresión, decisiones y ciclos. El analizador verifica su forma, sin ejecutar el programa ni verificar su significado.

## Elementos léxicos

Palabras reservadas: `int`, `float`, `string`, `bool`, `print`, `if`, `else`, `while`, `true`, `false`. No pueden utilizarse como nombres de variables. El lenguaje distingue mayúsculas y minúsculas.

| Tipo | Uso previsto | Ejemplo |
| --- | --- | --- |
| int | Enteros | `int edad = 20;` |
| float | Decimales | `float promedio = 85.5;` |
| string | Cadenas | `string nombre = "Erick";` |
| bool | Booleanos | `bool activo = true;` |

Los tipos indican la intención del programa; el analizador no comprueba compatibilidad entre el tipo y el valor.

- Identificadores: `[A-Za-z_][A-Za-z0-9_]*`, por ejemplo `edad`, `_total` y `dato2`.
- Números: `[0-9]+(\.[0-9]+)?`. Ejemplos: `20`, `0`, `85.5`. No se admiten `.5`, `5.` ni notación exponencial. El signo es un operador separado.
- Cadenas: texto entre comillas dobles, en una sola línea. Se permiten cadenas vacías y los escapes `\"`, `\\`, `\n`, `\t`, `\r`. Los escapes se reconocen, pero no se evalúan.
- Booleanos: `true` y `false`.
- Espacios, tabulaciones y saltos de línea separan elementos y se ignoran. Cada token conserva su línea y columna, desde 1.
- No se admiten comentarios. Los caracteres ajenos al lenguaje y las cadenas sin cierre producen errores léxicos.

## Operadores y precedencia

De menor a mayor prioridad:

| Nivel | Operadores | Categoría |
| --- | --- | --- |
| 1 | `\|\|` | Disyunción lógica |
| 2 | `&&` | Conjunción lógica |
| 3 | `==`, `!=` | Igualdad |
| 4 | `>`, `<`, `>=`, `<=` | Comparación |
| 5 | `+`, `-` | Suma y resta |
| 6 | `*`, `/`, `%` | Multiplicación, división y módulo |
| 7 | `!`, `+`, `-` | Operadores unarios |
| 8 | `(expresión)` | Agrupación explícita |

Los binarios del mismo nivel se reconocen en secuencia de izquierda a derecha; los unarios se anidan a la derecha. `=` corresponde a inicialización o asignación, no a una expresión. Por ejemplo, `10 + 5 * 2` agrupa la multiplicación antes de la suma. El parser no calcula el resultado.

## Sentencias

Las declaraciones permiten una inicialización opcional: `int contador;` o `int contador = 0;`. La asignación requiere un nombre y una expresión: `contador = contador + 1;`.

`print` requiere exactamente una expresión entre paréntesis y termina con punto y coma: `print("Hola mundo");` o `print(edad);`.

`if` requiere una condición entre paréntesis y un bloque entre llaves. Puede tener un `else` con otro bloque:

```text
if (edad >= 18) {
    print("Mayor");
} else {
    print("Menor");
}
```

`while` también requiere paréntesis y llaves:

```text
while (contador < 10) {
    contador = contador + 1;
}
```

Los bloques pueden estar vacíos o contener sentencias anidadas. No se añade `;` después del bloque. `else if` no es una producción directa: se puede escribir un `if` dentro del bloque `else`.

## Gramática completa (EBNF)

`*` significa cero o más repeticiones, `?` significa opcional y `|` indica alternativas. Los símbolos entre comillas son texto literal del lenguaje; los paréntesis sin comillas agrupan reglas.

```text
programa      -> sentencia* EOF
sentencia     -> declaracion | asignacion | impresion | condicional | mientras
declaracion   -> tipo IDENTIFIER ("=" expresion)? ";"
tipo          -> "int" | "float" | "string" | "bool"
asignacion    -> IDENTIFIER "=" expresion ";"
impresion     -> "print" "(" expresion ")" ";"
condicional   -> "if" "(" expresion ")" bloque ("else" bloque)?
mientras      -> "while" "(" expresion ")" bloque
bloque        -> "{" sentencia* "}"
expresion     -> disyuncion
disyuncion    -> conjuncion ("||" conjuncion)*
conjuncion    -> igualdad ("&&" igualdad)*
igualdad      -> comparacion (("==" | "!=") comparacion)*
comparacion   -> termino ((">" | "<" | ">=" | "<=") termino)*
termino       -> factor (("+" | "-") factor)*
factor        -> unaria (("*" | "/" | "%") unaria)*
unaria        -> ("!" | "+" | "-") unaria | primaria
primaria      -> NUMBER | STRING | BOOLEAN | IDENTIFIER | "(" expresion ")"
```

## Tokens del lexer

```text
TYPE IDENTIFIER NUMBER STRING BOOLEAN IF ELSE WHILE PRINT
PLUS MINUS MULTIPLY DIVIDE MODULO ASSIGN EQUAL NOT_EQUAL
GREATER LESS GREATER_EQUAL LESS_EQUAL AND OR NOT
LPAREN RPAREN LBRACE RBRACE SEMICOLON EOF
```

`TYPE` agrupa los cuatro tipos. `NUMBER` agrupa enteros y decimales. El valor del token conserva el texto original, incluidas las comillas de las cadenas. Los operadores de dos caracteres se reconocen antes que los de uno, evitando dividir `>=` en `>` y `=`. EOF marca el final de la entrada.

## Ejemplos de expresiones

```text
int resultado = 10 + 5 * 2;
float total = precio * cantidad;
bool mayor = edad >= 18;
bool permitido = !bloqueado && (mayor || autorizado);
int resto = (20 - 3) % 5;
```

## Diagnósticos

Un error léxico señala texto que no puede convertirse en tokens. Un error sintáctico señala tokens reconocidos que no cumplen una regla. Se muestra el primer error, con línea, elemento encontrado, elemento esperado y explicación. En errores sintácticos al final del archivo se señala la última línea con tokens, para facilitar la ubicación del elemento faltante.

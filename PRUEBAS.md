# Pruebas de MiniSyntax

Pega cada programa por separado en el editor y pulsa **Analizar**. Los números de línea se cuentan desde la primera línea de cada bloque. Los casos válidos deben mostrar **CORRECTO · Sintaxis válida**; los inválidos, **ERROR** con el diagnóstico indicado. No se espera que `print` ejecute una impresión.

## Programas con sintaxis correcta

### V1. Tipos e inicialización opcional

```text
int edad = 20;
float promedio = 85.5;
string nombre = "Erick";
bool activo = true;
int contador;
```

### V2. Asignación y precedencia aritmética

```text
int contador = 0;
contador = contador + 1;
int resultado = 10 + 5 * 2;
float total = (resultado - 2) / 4;
int resto = resultado % 3;
```

### V3. Impresión y decisión sin else

```text
int edad = 20;
print("Hola mundo");
if (edad >= 18) {
    print(edad);
}
```

### V4. Decisión con else y operadores lógicos

```text
int edad = 17;
bool activo = false;
if (edad >= 18 && !activo || edad == 17) {
    print("Mayor");
} else {
    print("Menor");
}
```

### V5. Ciclo y bloques anidados

```text
int contador = 0;
while (contador < 10) {
    if (contador != 5) {
        print(contador);
    }
    contador = contador + 1;
}
```

### V6. Signos unarios, comparación y cadenas escapadas

```text
int valor = -5 + +2;
bool prueba = valor <= 0 && valor > -10;
string mensaje = "Dijo: \"Hola\"";
print(mensaje);
```

## Programas con errores sintácticos

### E1. Falta punto y coma

```text
int edad = 20
```

Esperado: línea 1, encontrado EOF, esperado `;`. «Se esperaba ';' después de la declaración».

### E2. Falta paréntesis de cierre

```text
print(edad;
```

Esperado: línea 1, encontrado `;` (SEMICOLON), esperado `)`. «Se esperaba ')' para cerrar print».

### E3. Falta paréntesis después de if

```text
if edad > 18 {
    print(edad);
}
```

Esperado: línea 1, encontrado `edad` (IDENTIFIER), esperado `(` después de if.

### E4. Falta identificador

```text
int = 20;
```

Esperado: línea 1, encontrado `=` (ASSIGN), esperado un identificador después del tipo.

### E5. Falta operando

```text
int resultado = 10 + ;
```

Esperado: línea 1, encontrado `;` (SEMICOLON), esperada una expresión o un operando.

### E6. Falta llave de cierre

```text
while (contador < 10) {
    contador = contador + 1;
```

Esperado: línea 2 (última línea con tokens), encontrado EOF, esperada `}` para cerrar el bloque.

### E7. else sin if

```text
else {
    print("Hola");
}
```

Esperado: línea 1, encontrado `else` (ELSE), esperado el inicio de una sentencia.

## Errores léxicos adicionales

### L1. Cadena sin cerrar

```text
string nombre = "Erick;
```

Esperado: error léxico en línea 1, cadena sin comilla de cierre.

### L2. Carácter no reconocido

```text
int numero = 2 @ 3;
```

Esperado: error léxico en línea 1, carácter `@` no reconocido.

## Casos límite y alcance

- Entrada vacía: válida según `sentencia*`.
- `if (true) {}`: válido, bloque vacío.
- `print();`: inválido, falta expresión.
- `int if = 1;`: inválido, palabra reservada en lugar de identificador.
- `float total = precio * cantidad;`: válido; no se comprueba declaración de variables.
- `int dato = "texto";`: sintácticamente válido; no se comprueba compatibilidad de tipos.
- `print(1 / 0);`: sintácticamente válido; no se ejecuta la división.
- `int n = 5.;`: error léxico, faltan dígitos después del punto.

## Comprobación de la interfaz

1. Cargar ejemplo y analizar: resultado correcto.
2. Quitar un punto y coma y analizar: error y línea resaltada.
3. Editar el código: el resultado pasa a pendiente de análisis.
4. Limpiar: editor vacío y contador en 1 línea.
5. Pegar un programa de muchas líneas: comprobar numeración y desplazamiento vertical y horizontal.
6. Redimensionar la ventana: editor y resultados se adaptan.
7. Analizar usando Ctrl+Enter: mismo resultado que con el botón.

## Verificación realizada

Se revisó la sintaxis de los tres módulos con Python 3.12 y se ejecutaron los 15 programas documentados (6 válidos, 7 errores sintácticos y 2 errores léxicos), todos con el resultado esperado. También se verificaron 13 casos adicionales, el reconocimiento de operadores compuestos y las posiciones de tokens con saltos de línea de Windows.

Una prueba de integración creó la ventana real de Tkinter y comprobó las acciones de cargar ejemplo, analizar y limpiar, el resaltado de errores, la invalidación del resultado al editar, el contador con 150 líneas, el desplazamiento y el redimensionamiento. El empaquetado con PyInstaller no se ejecutó.

Erick 1-21-2841

# MiniSyntax - Analizador Sintáctico

Aplicación gráfica de escritorio para escribir o pegar programas de un pequeño lenguaje educativo y comprobar su estructura sintáctica. Toda la interacción ocurre en una ventana de Tkinter.


## Tecnologías 

Bueno quise utilizar las sigtes tecnologias:

- Python 3.10 o posterior (verificado con Python 3.12).
- Tkinter y ttk, incluidos en la instalación oficial de Python para Windows si se selecciona el componente Tcl/Tk.
- Biblioteca estándar: no se necesitan paquetes externos para ejecutar la aplicación.
- Compatible con Windows 11.

## Estructura del proyecto

| Archivo | Responsabilidad |
| --- | --- |
| `main.py` | Ventana, editor, numeración de líneas, botones y resultados. |
| `lexer.py` | Clase Token, Lexer y LexerError; conserva línea y columna. |
| `parser.py` | Parser descendente recursivo y ParserError; comprueba la gramática. |
| `GRAMATICA.md` | Especificación del lenguaje y precedencia de operadores. |
| `PRUEBAS.md` | Programas válidos e inválidos con resultados esperados. |

Flujo: **editor → Lexer.tokenize() → Parser.parse() → resultado en la ventana**.

El lexer entrega una lista de tokens terminada en EOF. El parser consume esa lista mediante métodos como `declaration`, `block` y `expression`. Cada nivel de expresión corresponde a una precedencia. La interfaz captura los errores de ambos módulos y resalta la línea correspondiente.

## Cómo ejecutar en Windows 11

Guarda los seis archivos en la misma carpeta. Abre PowerShell en esa carpeta y ejecuta:

```powershell
py -3 main.py
```

Si utilizas el comando `python` en lugar del lanzador `py`:

```powershell
python main.py
```

Estos comandos abren la ventana; no hay entrada ni salida de usuario por consola. Para abrirla sin una ventana de consola adicional, desde PowerShell puedes usar:

```powershell
pythonw main.py
```

Si falta Python, instala Python 3.10 o posterior con Tcl/Tk desde python.org. No intentes instalar Tkinter mediante pip.

## Uso

1. Escribe o pega un programa, o pulsa **Cargar ejemplo**.
2. Pulsa **Analizar** o **Ctrl+Enter**.
3. Lee el resultado: **CORRECTO** en verde o **ERROR** en rojo.
4. Si existe un error, revisa la línea resaltada y el token esperado. Corrígelo y analiza otra vez.
5. **Limpiar** vacía el editor. Al modificar código, el resultado anterior queda pendiente de un nuevo análisis.

Ejemplo válido:

```text
int edad = 20;
if (edad >= 18) {
    print("Mayor de edad");
}
```

Ejemplo inválido: `int edad = 20` necesita `;` al final. Consulta PRUEBAS.md para más casos.

## Alcance y límites

Se informa el primer error detectado. No se construye un árbol sintáctico ni se ejecutan instrucciones. `print` se reconoce como sentencia, pero no imprime valores. No hay tabla de símbolos, comprobación de tipos ni detección de variables no declaradas: `float total = precio * cantidad;` es sintácticamente válido aunque esas variables no estén declaradas. Tampoco se evalúan divisiones por cero o condiciones.

El programa vacío y los bloques vacíos son válidos. El lenguaje distingue mayúsculas y minúsculas. No admite comentarios, funciones, listas, incrementos `++` ni asignaciones dentro de expresiones. El anidamiento excesivo puede alcanzar el límite de recursión de Python; la ventana informa esa limitación sin afirmar que sea un error gramatical.

## Conversión opcional a ejecutable

PyInstaller solo se necesita al empaquetar, no durante el uso normal. Desde la carpeta del proyecto:

```powershell
py -3 -m pip install pyinstaller
py -3 -m PyInstaller --onefile --windowed --name MiniSyntax main.py
```

El ejecutable se genera en `dist\MiniSyntax.exe`. La opción `--windowed` evita la consola. Genera el ejecutable en Windows para distribuirlo en Windows y pruébalo en el equipo de destino.

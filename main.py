"""Interfaz gráfica de MiniSyntax. Ejecutar este archivo para abrir la app."""

import tkinter as tk
from tkinter import ttk

from lexer import Lexer, LexerError
from parser import Parser, ParserError


EXAMPLE = '''int edad = 20;
float promedio = 85.5;
string nombre = "Erick";
bool activo = true;
int contador;
contador = 0;

if (edad >= 18 && activo) {
    print("Mayor de edad");
} else {
    print("Menor de edad");
}

while (contador < 10) {
    contador = contador + 1;
}

int resultado = 10 + 5 * 2;
print(resultado);
'''


class MiniSyntaxApp:
    def __init__(self, root):
        self.root = root
        root.title("Analizador Sintáctico")
        root.geometry("1000x740")
        root.minsize(700, 520)
        root.configure(bg="#f2f2f2")

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="#b7d8e0")
        style.configure("TLabel", background="#f2f2f2", foreground="#243247", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 5))
        style.configure("Analyze.TButton", background="#2563eb", foreground="white")
        style.map("Analyze.TButton", background=[("active", "#1d4ed8")])

        body = ttk.Frame(root, padding=16)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(3, weight=3)
        body.rowconfigure(7, weight=1)
        ttk.Label(body, text="Analizador Sintáctico", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12))

        toolbar = ttk.Frame(body)
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        ttk.Button(toolbar, text="Analizar", style="Analyze.TButton", command=self.analyze).pack(side="left")
        ttk.Button(toolbar, text="Limpiar", command=self.clear).pack(side="left", padx=8)
        ttk.Button(toolbar, text="Cargar ejemplo", command=self.load_example).pack(side="left")
        ttk.Label(body, text="Código fuente").grid(row=2, column=0, sticky="w", pady=(0, 6))

        editor_frame = ttk.Frame(body)
        editor_frame.grid(row=3, column=0, sticky="nsew")
        editor_frame.rowconfigure(0, weight=1)
        editor_frame.columnconfigure(1, weight=1)
        self.gutter = tk.Canvas(editor_frame, width=52, bg="#e8e8e8", highlightthickness=0)
        self.gutter.grid(row=0, column=0, sticky="ns")
        self.editor = tk.Text(editor_frame, wrap="none", undo=True, font=("Consolas", 12),
                              bg="#ffffff", fg="#182438", insertbackground="#2563eb",
                              padx=10, pady=8, relief="flat", tabs=(40,))
        self.editor.grid(row=0, column=1, sticky="nsew")
        vertical = ttk.Scrollbar(editor_frame, orient="vertical", command=self.editor.yview)
        vertical.grid(row=0, column=2, sticky="ns")
        horizontal = ttk.Scrollbar(editor_frame, orient="horizontal", command=self.editor.xview)
        horizontal.grid(row=1, column=1, sticky="ew")
        self.editor.configure(yscrollcommand=lambda a, b: self.on_scroll(vertical, a, b),
                              xscrollcommand=horizontal.set)
        self.editor.tag_configure("error", background="#fee2e2")
        self.editor.bind("<<Modified>>", self.on_modified)
        self.editor.bind("<Configure>", lambda event: self.redraw_lines())
        root.bind("<Control-Return>", self.analyze)

        self.line_count = ttk.Label(body, text="1 línea")
        self.line_count.grid(row=4, column=0, sticky="e", pady=5)
        ttk.Label(body, text="Resultado del análisis").grid(row=5, column=0, sticky="w", pady=(6, 0))
        self.status = tk.StringVar(value="Listo para analizar")
        self.status_label = ttk.Label(body, textvariable=self.status, font=("Segoe UI", 11, "bold"))
        self.status_label.grid(row=6, column=0, sticky="w", pady=(6, 6))
        result_frame = ttk.Frame(body)
        result_frame.grid(row=7, column=0, sticky="nsew")
        self.result = tk.Text(result_frame, height=7, wrap="word", font=("Consolas", 11),
                              bg="#ffffff", fg="#243247", padx=12, pady=10, relief="flat", state="disabled")
        result_scroll = ttk.Scrollbar(result_frame, command=self.result.yview)
        result_scroll.pack(side="right", fill="y")
        self.result.pack(fill="both", expand=True)
        self.result.configure(yscrollcommand=result_scroll.set)
        self.show_result("Escribe código o pulsa «Cargar ejemplo». El análisis no ejecuta el programa.")
        self.editor.focus_set()

    def show_result(self, text):
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)
        self.result.configure(state="disabled")

    def on_scroll(self, scrollbar, first, last):
        scrollbar.set(first, last)
        self.redraw_lines()

    def redraw_lines(self):
        self.gutter.delete("all")
        index = self.editor.index("@0,0")
        while True:
            info = self.editor.dlineinfo(index)
            if info is None:
                break
            self.gutter.create_text(43, info[1], anchor="ne", text=index.split(".")[0],
                                    fill="#64748b", font=("Consolas", 12))
            index = self.editor.index(f"{index}+1line")

    def on_modified(self, event=None):
        if self.editor.edit_modified():
            self.editor.edit_modified(False)
            count = int(self.editor.index("end-1c").split(".")[0])
            self.line_count.configure(text=f"{count} línea" if count == 1 else f"{count} líneas")
            self.editor.tag_remove("error", "1.0", "end")
            self.status.set("Código modificado · pendiente de análisis")
            self.status_label.configure(foreground="#243247")
            self.show_result("Pulsa «Analizar» para comprobar el código actual.")
            self.root.after_idle(self.redraw_lines)

    def analyze(self, event=None):
        # Procesar la modificación pendiente antes de mostrar el resultado nuevo.
        self.on_modified()
        self.editor.tag_remove("error", "1.0", "end")
        source = self.editor.get("1.0", "end-1c")
        try:
            tokens = Lexer(source).tokenize()
            Parser(tokens).parse()
        except (LexerError, ParserError) as error:
            self.status.set("ERROR · Revisa el código")
            self.status_label.configure(foreground="#b91c1c")
            self.show_result(str(error))
            self.editor.tag_add("error", f"{error.line}.0", f"{error.line}.end")
            self.editor.see(f"{error.line}.0")
        except RecursionError:
            self.status.set("LÍMITE DE ANÁLISIS")
            self.status_label.configure(foreground="#b91c1c")
            self.show_result("El código tiene demasiados niveles anidados. Reduce el anidamiento y vuelve a analizar.")
        else:
            self.status.set("CORRECTO · Sintaxis válida")
            self.status_label.configure(foreground="#15803d")
            message = f"El código cumple la gramática de MiniSyntax.\nTokens analizados: {len(tokens) - 1}."
            if not source.strip():
                message += "\nEl programa vacío es válido: programa → sentencia*."
            self.show_result(message + "\nSolo se comprueba la sintaxis; no se ejecuta ni se verifican tipos o variables.")
        return "break"

    def clear(self):
        self.editor.delete("1.0", "end")
        self.on_modified()
        self.status.set("Listo para analizar")
        self.show_result("Escribe código o pulsa «Cargar ejemplo».")
        self.editor.focus_set()

    def load_example(self):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", EXAMPLE)
        self.editor.focus_set()
        self.editor.see("1.0")


if __name__ == "__main__":
    window = tk.Tk()
    MiniSyntaxApp(window)
    window.mainloop()

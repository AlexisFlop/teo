# -*- coding: utf-8 -*-
# Ejecuta tu MISMO parser sobre frases de lenguaje natural para ver fallas claras

from parser import Parser

CASES = [
    # sin ;, ni tipos, ni sintaxis C — deben fallar
    "the dog sleeps",
    "the dog sees a man with a telescope",
    "hola mundo",
    "imprime 3 + 4",
    "(the cat)",
    # incluso si agregas ; seguirá fallando por tokens desconocidos
    "the dog sleeps;",
    "int henry;"
]


def run():
    for i, src in enumerate(CASES, 1):
        print("\n" + "=" * 70)
        print(f"[Caso {i}] {src!r}")
        try:
            Parser(src).parse()
            print("⚠️  El parser NO falló (sorprendente). Revisa tu gramática.")
        except SyntaxError as e:
            print("❌ Falla documentada:")
            print("   ", e)


if __name__ == "__main__":
    run()

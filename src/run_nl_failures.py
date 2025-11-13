from parser import Parser

CASES = [
    "the dog sleeps",
    "the dog sees a man with a telescope",
    "hola mundo",
    "imprime 3 + 4",
    "(the cat)"
]


def run():
    for i, src in enumerate(CASES, 1):
        print("\n" + "=" * 70)
        print(f"[Caso {i}] {src!r}")
        try:
            Parser(src).parse()
            print("Parser ejecutado con exito")
        except SyntaxError as e:
            print("Errores:")
            print("   ", e)


if __name__ == "__main__":
    run()

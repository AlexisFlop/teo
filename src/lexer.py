import ply.lex as lex

PROGRAM = 0
DECLARATION = 1
TYPE = 2
VAR_LIST = 3
MORE_VARS = 4
STATEMENT = 5
ASSIGNMENT = 6
EXPRESSION = 7
TERM = 8
FACTOR = 9

tokens = (
    'NUMBER',
    'FLOAT_NUMBER',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'ASSIGN',
    'CHAR',
    'FLOAT_TYPE',
    'CHAR_TYPE',
    'STRING_TYPE',
    'IDENTIFIER',
    'EOF'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_ASSIGN = r'='


def t_FLOAT_TYPE(t):
    r'float'
    return t


def t_CHAR_TYPE(t):
    r'char'
    return t


def t_STRING_TYPE(t):
    r'string'
    return t


def t_FLOAT_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHAR(t):
    r"'[^']'"
    return t


def t_STRING(t):
    r'\"[^\"]*\"'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


t_ignore = ' \t'


def t_error(t):
    print(f"Caracter no valido: {t.value[0]}")
    t.lexer.skip(1)


tabla = [
    [PROGRAM, 'FLOAT_TYPE', [DECLARATION, STATEMENT, 'EOF']],
    [PROGRAM, 'CHAR_TYPE', [DECLARATION, STATEMENT, 'EOF']],
    [PROGRAM, 'STRING_TYPE', [DECLARATION, STATEMENT, 'EOF']],
    [PROGRAM, 'IDENTIFIER', [DECLARATION, STATEMENT, 'EOF']],
    [PROGRAM, 'EOF', ['EOF']],

    [DECLARATION, 'FLOAT_TYPE', [TYPE, VAR_LIST, 'SEMICOLON']],
    [DECLARATION, 'CHAR_TYPE', [TYPE, VAR_LIST, 'SEMICOLON']],
    [DECLARATION, 'STRING_TYPE', [TYPE, VAR_LIST, 'SEMICOLON']],
    [DECLARATION, 'IDENTIFIER', []],
    [DECLARATION, 'EOF', []],

    [TYPE, 'FLOAT_TYPE', ['FLOAT_TYPE']],
    [TYPE, 'CHAR_TYPE', ['CHAR_TYPE']],
    [TYPE, 'STRING_TYPE', ['STRING_TYPE']],

    [VAR_LIST, 'IDENTIFIER', ['IDENTIFIER', MORE_VARS]],

    [MORE_VARS, 'COMMA', ['COMMA', 'IDENTIFIER', MORE_VARS]],
    [MORE_VARS, 'SEMICOLON', []],

    [STATEMENT, 'IDENTIFIER', [ASSIGNMENT, 'SEMICOLON', STATEMENT]],
    [STATEMENT, 'EOF', []],

    [ASSIGNMENT, 'IDENTIFIER', ['IDENTIFIER', 'ASSIGN', EXPRESSION]],

    [EXPRESSION, 'STRING', [TERM, EXPRESSION]],
    [EXPRESSION, 'IDENTIFIER', [TERM, EXPRESSION]],
    [EXPRESSION, 'NUMBER', [TERM, EXPRESSION]],
    [EXPRESSION, 'FLOAT_NUMBER', [TERM, EXPRESSION]],
    [EXPRESSION, 'LPAREN', [TERM, EXPRESSION]],
    [EXPRESSION, 'PLUS', ['PLUS', TERM, EXPRESSION]],
    [EXPRESSION, 'MINUS', ['MINUS', TERM, EXPRESSION]],
    [EXPRESSION, 'SEMICOLON', []],
    [EXPRESSION, 'RPAREN', []],

    [TERM, 'STRING', [FACTOR, TERM]],
    [TERM, 'IDENTIFIER', [FACTOR, TERM]],
    [TERM, 'NUMBER', [FACTOR, TERM]],
    [TERM, 'FLOAT_NUMBER', [FACTOR, TERM]],
    [TERM, 'LPAREN', [FACTOR, TERM]],
    [TERM, 'TIMES', ['TIMES', FACTOR, TERM]],
    [TERM, 'DIVIDE', ['DIVIDE', FACTOR, TERM]],
    [TERM, 'PLUS', []],
    [TERM, 'MINUS', []],
    [TERM, 'SEMICOLON', []],
    [TERM, 'RPAREN', []],


    [FACTOR, 'STRING', ['STRING']],
    [FACTOR, 'IDENTIFIER', ['IDENTIFIER']],
    [FACTOR, 'NUMBER', ['NUMBER']],
    [FACTOR, 'FLOAT_NUMBER', ['FLOAT_NUMBER']],
    [FACTOR, 'LPAREN', ['LPAREN', EXPRESSION, 'RPAREN']],
]

lexer = lex.lex()

stack = ['EOF', PROGRAM]


def searchProduction(no_terminal, terminal):
    return next((fila[2] for fila in tabla if fila[0] == no_terminal and fila[1] == terminal), None)


def stackProduction(produccion):
    list(map(lambda elem: stack.append(elem) if elem != '' else None, reversed(produccion)))


def codeAnalyzer(expression):
    lexer.input(expression)
    tok = lexer.token() or type('Token', (), {'type': 'EOF', 'value': '$'})()

    x = stack[-1]

    print(f"Analizando: {expression}")

    while True:
        print(f"Pila: {stack}, Token: {tok.type}='{tok.value}'")

        if x == 'EOF' and tok.type == 'EOF':
            print("Analisis completado")
            return True

        if x in tokens and x == tok.type:
            stack.pop()
            print(f"Token reconocido: {x}")
            tok = lexer.token() or type('Token', (), {'type': 'EOF', 'value': '$'})()
            x = stack[-1] if stack else 'EOF'

        elif x in tokens:
            print(f"Error: se esperaba {x} pero se encontro {tok.type}")
            return False

        else:
            produccion = searchProduction(x, tok.type)
            if produccion is None:
                print(f"Error")
                return False

            stack.pop()
            if produccion:
                stackProduction(produccion)
            x = stack[-1] if stack else 'EOF'


examples = [
    "float x;",
    "float a, b; a = a*b;",
    "string flamenco ; flamenco = \"Flamenco\";",
    #Pruebas NLP
    "henry alexis flores",
    "El perro de Juan es oscuro",
    "Una vaca vestida de uniforme",
    "Vamos a pasar TEO(?"
]

print("=== PARSER LL(1) ===")
for i, codigo in enumerate(examples, 1):
    print(f"\n--- Ejemplo {i} ---")
    stack = ['EOF', PROGRAM]
    lexer.lineno = 1
    resultado = codeAnalyzer(codigo)
    print(f"Resultado: {'OK' if resultado else 'ERROR'}")
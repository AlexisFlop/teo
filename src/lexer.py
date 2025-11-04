from dataclasses import dataclass
import re

TT_INT = "INT_KW"
TT_FLOAT = "FLOAT_KW"
TT_RETURN = "RETURN_KW"
TT_PRINT = "PRINT_KW"

TT_ID = "ID"
TT_NUM = "NUM"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_STAR = "STAR"
TT_SLASH = "SLASH"
TT_ASSIGN = "ASSIGN"

TT_SEMI = "SEMI"
TT_COMMA = "COMMA"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"

TT_EOF = "EOF"

TOKEN_REGEX = [
    (r"[ \t\r\n]+", None),  # espacios
    (r"\bint\b", TT_INT),
    (r"\bfloat\b", TT_FLOAT),
    (r"\breturn\b", TT_RETURN),
    (r"\bprint\b", TT_PRINT),

    (r"[a-zA-Z_][a-zA-Z0-9_]*", TT_ID),
    (r"\d+(?:\.\d+)?", TT_NUM),

    (r"\+", TT_PLUS),
    (r"-", TT_MINUS),
    (r"\*", TT_STAR),
    (r"/", TT_SLASH),
    (r"=", TT_ASSIGN),

    (r";", TT_SEMI),
    (r",", TT_COMMA),
    (r"\(", TT_LPAREN),
    (r"\)", TT_RPAREN),
    (r"\{", TT_LBRACE),
    (r"\}", TT_RBRACE),
]


@dataclass
class Token:
    type: str
    lexeme: str
    pos: int


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.patterns = [(re.compile(pat, re.DOTALL), typ) for pat, typ in TOKEN_REGEX]

    def next_token(self) -> Token:
        if self.pos >= len(self.text):
            return Token(TT_EOF, "", self.pos)

        for regex, typ in self.patterns:
            m = regex.match(self.text, self.pos)
            if m:
                lex = m.group(0)
                start = self.pos
                self.pos = m.end()
                if typ is None:
                    # ignorar espacios
                    return self.next_token()
                return Token(typ, lex, start)

        snippet = self.text[self.pos:self.pos + 20].replace("\n", "\\n")
        raise SyntaxError(f"Caracter inesperado en posición {self.pos}: '{snippet}'")

from ast_nodes import *
from lexer import (
    Lexer, Token,
    TT_INT, TT_FLOAT, TT_RETURN, TT_PRINT,
    TT_ID, TT_NUM,
    TT_PLUS, TT_MINUS, TT_STAR, TT_SLASH,
    TT_ASSIGN, TT_SEMI, TT_COMMA,
    TT_LPAREN, TT_RPAREN, TT_LBRACE, TT_RBRACE, TT_EOF
)


class Parser:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.current: Token = self.lexer.next_token()

    def _eat(self, expected_type: str) -> Token:
        if self.current.type == expected_type:
            tok = self.current
            self.current = self.lexer.next_token()
            return tok
        self._error_expected(expected_type)

    def _error_expected(self, expected: str):
        raise SyntaxError(
            f"Se esperaba {expected} pero llegó {self.current.type} "
            f"('{self.current.lexeme}') en pos {self.current.pos}"
        )

    def _lookahead_is(self, ttype: str) -> bool:
        return self.current.type == ttype

    def parse(self) -> ProgramNode:
        items: List[TopLevel] = []
        while self.current.type != TT_EOF:
            if self._lookahead_is(TT_INT) or self._lookahead_is(TT_FLOAT):

                save = self.current
                retype = self._type_spec()  # consume type
                if self._lookahead_is(TT_ID):
                    name_tok = self._eat(TT_ID)
                    if self._lookahead_is(TT_LPAREN):

                        self._eat(TT_LPAREN)
                        params = self._params_opt()
                        self._eat(TT_RPAREN)
                        body = self._block()
                        items.append(FuncDecl(retype, name_tok.lexeme, params, body))
                    else:

                        self._eat(TT_SEMI)
                        items.append(DeclNode(retype, name_tok.lexeme))
                else:
                    self._error_expected("id")
            else:
                items.append(self._stmt_like())
        return ProgramNode(items)

    def _block(self) -> Block:
        self._eat(TT_LBRACE)
        items: List = []
        while not self._lookahead_is(TT_RBRACE):
            if self._lookahead_is(TT_INT) or self._lookahead_is(TT_FLOAT):
                vary = self._type_spec()
                name = self._eat(TT_ID).lexeme
                self._eat(TT_SEMI)
                items.append(DeclNode(vary, name))
            elif self._lookahead_is(TT_PRINT):
                items.append(self._print_stmt())
            elif self._lookahead_is(TT_RETURN):
                items.append(self._return_stmt())
            else:
                items.append(self._stmt())
        self._eat(TT_RBRACE)
        return Block(items)

    def _params_opt(self) -> List[Param]:
        params: List[Param] = []
        if self._lookahead_is(TT_INT) or self._lookahead_is(TT_FLOAT):
            vary = self._type_spec()
            name = self._eat(TT_ID).lexeme
            params.append(Param(vary, name))
            while self._lookahead_is(TT_COMMA):
                self._eat(TT_COMMA)
                vary = self._type_spec()
                name = self._eat(TT_ID).lexeme
                params.append(Param(vary, name))
        return params

    def _type_spec(self) -> str:
        if self._lookahead_is(TT_INT):
            self._eat(TT_INT)
            return "int"
        if self._lookahead_is(TT_FLOAT):
            self._eat(TT_FLOAT)
            return "float"
        self._error_expected("int|float")

    def _stmt_like(self) -> TopLevel:
        if self._lookahead_is(TT_PRINT):
            return self._print_stmt()
        if self._lookahead_is(TT_RETURN):
            return self._return_stmt()
        return self._stmt()

    # Stmt → id '=' Expr ';' | Expr ';'
    def _stmt(self) -> Union[AssignNode, ExprNode]:

        if self._lookahead_is(TT_ID):

            name_tok = self._eat(TT_ID)
            if self._lookahead_is(TT_ASSIGN):
                self._eat(TT_ASSIGN)
                expr = self._expr()
                self._eat(TT_SEMI)
                return AssignNode(name_tok.lexeme, expr)
            elif self._lookahead_is(TT_LPAREN):
                args = self._call_args()
                self._eat(TT_SEMI)
                return CallNode(name_tok.lexeme, args)
            else:
                self._error_expected("'=' o '('")
        else:
            expr = self._expr()
            self._eat(TT_SEMI)
            return expr

    def _print_stmt(self) -> PrintStmt:
        self._eat(TT_PRINT)
        self._eat(TT_LPAREN)
        expr = self._expr()
        self._eat(TT_RPAREN)
        self._eat(TT_SEMI)
        return PrintStmt(expr)

    def _return_stmt(self) -> ReturnStmt:
        self._eat(TT_RETURN)
        expr: Optional[ExprNode] = None
        if not self._lookahead_is(TT_SEMI):
            expr = self._expr()
        self._eat(TT_SEMI)
        return ReturnStmt(expr)

    def _expr(self) -> ExprNode:
        node = self._term()
        while self._lookahead_is(TT_PLUS) or self._lookahead_is(TT_MINUS):
            op = self.current.lexeme
            self._eat(self.current.type)
            right = self._term()
            node = BinOpNode(op, node, right)
        return node

    def _term(self) -> ExprNode:
        node = self._factor()
        while self._lookahead_is(TT_STAR) or self._lookahead_is(TT_SLASH):
            op = self.current.lexeme
            self._eat(self.current.type)
            right = self._factor()
            node = BinOpNode(op, node, right)
        return node

    def _factor(self) -> ExprNode:
        if self._lookahead_is(TT_ID):
            name = self._eat(TT_ID).lexeme
            if self._lookahead_is(TT_LPAREN):
                args = self._call_args()
                return CallNode(name, args)
            return IdNode(name)
        if self._lookahead_is(TT_NUM):
            return NumNode(self._eat(TT_NUM).lexeme)
        if self._lookahead_is(TT_LPAREN):
            self._eat(TT_LPAREN)
            node = self._expr()
            self._eat(TT_RPAREN)
            return node
        self._error_expected("id|num|'('")

    def _call_args(self) -> List[ExprNode]:
        self._eat(TT_LPAREN)
        args: List[ExprNode] = []
        if not self._lookahead_is(TT_RPAREN):
            args.append(self._expr())
            while self._lookahead_is(TT_COMMA):
                self._eat(TT_COMMA)
                args.append(self._expr())
        self._eat(TT_RPAREN)
        return args


class ReturnSignal(Exception):
    def __init__(self, value): self.value = value


class Interpreter:
    def __init__(self, program: ProgramNode):
        self.program = program
        self.functions: dict[str, FuncDecl] = {}
        self.globals: dict[str, float] = {}

        for it in program.items:
            if isinstance(it, FuncDecl):
                self.functions[it.name] = it
            elif isinstance(it, DeclNode):
                self.globals[it.name] = 0.0
            elif isinstance(it, AssignNode):
                self.globals[it.name] = self._eval_expr(it.expr, self.globals)

    def call(self, name: str, args_vals: List[float]) -> float:
        if name not in self.functions:
            raise RuntimeError(f"Función no definida: {name}")
        f = self.functions[name]
        if len(args_vals) != len(f.params):
            raise RuntimeError(f"Aridad incorrecta para {name}")
        env = {p.name: v for p, v in zip(f.params, args_vals)}
        try:
            self._exec_block(f.body, env)
        except ReturnSignal as r:
            return float(r.value if r.value is not None else 0.0)
        return 0.0

    def _exec_block(self, block: Block, env: dict[str, float]) -> None:
        for it in block.items:
            if isinstance(it, DeclNode):
                env[it.name] = 0.0
            elif isinstance(it, AssignNode):
                env[it.name if it.name in env else self._resolve_scope(it.name, env)] = \
                    self._eval_expr(it.expr, env)
            elif isinstance(it, PrintStmt):
                val = self._eval_expr(it.expr, env)
                # PRINT REAL
                print(val)
            elif isinstance(it, ReturnStmt):
                val = self._eval_expr(it.expr, env) if it.expr is not None else 0.0
                raise ReturnSignal(val)
            else:
                if isinstance(it, ExprNode):
                    self._eval_expr(it, env)

    def _resolve_scope(self, name: str, env: dict[str, float]) -> str:
        if name in env:
            return name
        if name in self.globals:
            return name
        raise RuntimeError(f"Variable no declarada: {name}")

    def _eval_expr(self, node: ExprNode, env: dict[str, float]) -> float:
        if isinstance(node, NumNode):
            return float(node.value)
        if isinstance(node, IdNode):
            if node.name in env:
                return env[node.name]
            if node.name in self.globals:
                return self.globals[node.name]
            raise RuntimeError(f"Variable no declarada: {node.name}")
        if isinstance(node, BinOpNode):
            a = self._eval_expr(node.left, env)
            b = self._eval_expr(node.right, env)
            if node.op == "+": return a + b
            if node.op == "-": return a - b
            if node.op == "*": return a * b
            if node.op == "/": return a / b
            raise RuntimeError(f"Operador no soportado: {node.op}")
        if isinstance(node, CallNode):
            args_vals = [self._eval_expr(a, env) for a in node.args]
            return self.call(node.func, args_vals)
        return 0.0


# ---------------------- DEMO ----------------------

DEMO_SOURCE = r"""
float flamenco;
float h;

int add(int a, int b) {
    print(a + b);
    return a + b;
}

float twice(float x) {
    return x * 2;
}

int main(int z) {
    int t;
    t = add(3, 4);      
    print(t);           
    print(twice(5));     
    return 0;
}

g = 1 + 2;
"""


def _demo():
    try:
        parser = Parser(DEMO_SOURCE)
        ast = parser.parse()
        print("AST generado:\n")
        print_ast(ast)
        print("\n---- EJECUCIÓN ----")
        vm = Interpreter(ast)
        # llamar main “a mano”
        vm.call("main", [0])
    except (SyntaxError, RuntimeError) as e:
        print("Error:", e)


if __name__ == "__main__":
    _demo()

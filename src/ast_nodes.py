# -*- coding: utf-8 -*-
# Nodos del AST para el subconjunto extendido: declaraciones, funciones, llamadas y print

from dataclasses import dataclass
from typing import List, Union, Optional


# ---- Programa ----
@dataclass
class ProgramNode:
    items: List["TopLevel"]  # FuncDecl | DeclNode | AssignNode


TopLevel = Union["FuncDecl", "DeclNode", "AssignNode"]


# ---- Declaraciones / Sentencias ----
@dataclass
class DeclNode:
    vartype: str  # 'int' | 'float'
    name: str


@dataclass
class AssignNode:
    name: str
    expr: "ExprNode"


@dataclass
class PrintStmt:
    expr: "ExprNode"


@dataclass
class ReturnStmt:
    expr: Optional["ExprNode"]  # puede ser None


# ---- Funciones ----
@dataclass
class Param:
    vartype: str
    name: str


@dataclass
class Block:
    items: List[Union["DeclNode", "AssignNode", "PrintStmt", "ReturnStmt"]]


@dataclass
class FuncDecl:
    rettype: str  # 'int' | 'float'
    name: str
    params: List[Param]
    body: Block


# ---- Expresiones ----
class ExprNode: ...


@dataclass
class BinOpNode(ExprNode):
    op: str
    left: "ExprNode"
    right: "ExprNode"


@dataclass
class NumNode(ExprNode):
    value: str


@dataclass
class IdNode(ExprNode):
    name: str


@dataclass
class CallNode(ExprNode):
    func: str
    args: List["ExprNode"]


# ---- Utilidad: pretty print del AST ----
def print_ast(node, indent: int = 0) -> None:
    pad = "  " * indent
    if isinstance(node, ProgramNode):
        print(pad + "Program")
        for it in node.items:
            print_ast(it, indent + 1)

    elif isinstance(node, FuncDecl):
        print(pad + f"FuncDecl(ret={node.rettype}, name={node.name})")
        if node.params:
            print(pad + "  Params:")
            for p in node.params:
                print(pad + f"    Param(type={p.vartype}, name={p.name})")
        print(pad + "  Body:")
        print_ast(node.body, indent + 2)

    elif isinstance(node, Block):
        print(pad + "Block")
        for it in node.items:
            print_ast(it, indent + 1)

    elif isinstance(node, DeclNode):
        print(pad + f"Decl(type={node.vartype}, name={node.name})")

    elif isinstance(node, AssignNode):
        print(pad + f"Assign(name={node.name})")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, PrintStmt):
        print(pad + "Print")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, ReturnStmt):
        print(pad + "Return")
        if node.expr is not None:
            print_ast(node.expr, indent + 1)

    elif isinstance(node, BinOpNode):
        print(pad + f"BinOp(op='{node.op}')")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, NumNode):
        print(pad + f"Num({node.value})")

    elif isinstance(node, IdNode):
        print(pad + f"Id({node.name})")

    elif isinstance(node, CallNode):
        print(pad + f"Call({node.func})")
        for a in node.args:
            print_ast(a, indent + 1)

    else:
        print(pad + f"(nodo desconocido: {node})")

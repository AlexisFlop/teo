# -*- coding: utf-8 -*-
"""
Gramática extendida (sin rec. izquierda) para funciones, llamadas y print.

Program   → (Func | Decl | Stmt)* EOF

Func      → Type id '(' Params? ')' Block
Params    → Type id (',' Type id)*
Block     → '{' (Decl | Stmt | PrintStmt | ReturnStmt)* '}'

Decl      → Type id ';'
Type      → 'int' | 'float'

Stmt      → id '=' Expr ';'              # asignación
          | Expr ';'                     # permite 'foo(1,2);' como stmt

PrintStmt → 'print' '(' Expr ')' ';'
ReturnStmt→ 'return' Expr? ';'

Expr      → Term (('+'|'-') Term)*
Term      → Factor (('*'|'/') Factor)*
Factor    → id
          | num
          | '(' Expr ')'
          | id '(' Args? ')'            # llamada a función

Args      → Expr (',' Expr)*
"""
GRAMMAR_TEXT = __doc__

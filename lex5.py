# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:19:51 2017

@author: cedric.pahud
"""

import ply.lex as lex
from ply.lex import TOKEN

reserved_words = (
    'bpm',
    'start',
    'stop',
    'rep',
    'arp'
)

notes = (
    'do',
    're',
    'mi',
    'fa',
    'sol',
    'la',
    'si',
    'nop'
)

# notes avec chiffres
# notes = [f"{x}{y}" for x in notes for y in range(0,9)]

tokens =(
        'NUMBER',
        'NOTE',
        'ID',
)+ tuple(map(lambda s: s.upper(),reserved_words))

# t_ADD_OP = r'[+-]'
# t_MUL_OP = r'[/*]'

literals = r'();={}[],'

@TOKEN('|'.join(notes))
def t_NOTE(t):
    return t

# reconnais pas rep et autre
def t_ID(t):
    r'[A-Za-z_]\w*'
    print('LOL')
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno+=len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("illegal character '%s'"%t.value[0])
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)"%(tok.lineno, tok.type, tok.value))

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:19:51 2017

@author: cedric.pahud
"""

import ply.lex as lex
from ply.lex import TOKEN

reserved_words = (
    'BPM',
    'START',
    'STOP',
    'REP',
    'ARP'
)

notes = (
    'do',
    're',
    'mi',
    'fa',
    'sol',
    'la',
    'si'
)


tokens =(
        'NUMBER',
        'NOTE',
        'ID',
        'SIGNAL',
        'NEWLINE'
) + tuple(map(lambda s: s.upper(),reserved_words))


literals = r'();={}[],'

notes = [note+str(i) for note in notes for i in range(1,9) if note != "nop"]


@TOKEN(r'|'.join(notes))
def t_NOTE(t):
    return t

@TOKEN(r'|'.join(['sine','saw','pulse','square']))
def t_SIGNAL(t):
    return t

# peut être changer genre peu pas commencer par maj ou autre pour pas que ça empiète avec note
def t_ID(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno+=len(t.value)
    return t

def t_comment(t):
    r'\#.*\n*'
    t.lexer.lineno+=t.value.count('\n')

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

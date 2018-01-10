# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 10:06:43 2017

@author: cedric.pahud
"""

import ply.yacc as yacc
from lex5 import tokens
import AST

'''operations = {
        '+' : lambda x,y: x+y,
        '-' : lambda x,y: x-y,
        '*' : lambda x,y: x*y,
        '/' : lambda x,y: x/y,
        }'''



'''precedence = (
        ('left', 'ADD_OP'),
        ('left', 'MUL_OP'),
        ('right', 'UMINUS'), #uminus n'est pas un token mais il permet de définir la précédence d'une expression
)'''


def p_programme(p):
    '''programme : assignationBlock START NEWLINE codeBlock STOP'''
    p[0]=AST.ProgramNode([p[1],p[4]])

def p_codeBlock(p):
    '''codeBlock : statement NEWLINE'''
    p[0]=AST.codeBlockNode(p[1])

def p_codeBlock_rec(p):
    '''codeBlock : statement NEWLINE codeBlock'''
    p[0]=AST.codeBlockNode([p[1]]+p[3].children)

def p_assignation_block(p):
    '''assignationBlock : assignation NEWLINE'''
    p[0]= AST.AssignBlockNode(p[1])

def p_assignation_block_rec(p):
    '''assignationBlock : assignation NEWLINE assignationBlock'''
    p[0]= AST.AssignBlockNode([p[1]]+p[3].children)

def p_assignation(p):
    '''assignation : ID '=' expression'''
    p[0]=AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_expression(p):
    '''expression : ID
    | SIGNAL
    | NUMBER'''
    p[0]=AST.TokenNode(p[1])

def p_statement(p):
    '''statement : repetedBlock
    | instrPlay'''
    p[0]=p[1]

def p_repetedBlock(p):
    '''repetedBlock : REP '(' expression ')' NEWLINE '{' NEWLINE codeBlock '}' '''
    p[0]=AST.RepNode([p[3],p[8]])

def p_instrPlay(p):
    '''instrPlay : ID NOTE'''
    p[0]=AST.PlayNode([AST.TokenNode(p[1]),AST.TokenNode(p[2])])


def p_error(p):
    print ("Syntax error in line %d"%p.lineno)
    yacc.errok()

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys
    import os
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    print (result)
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to",name)

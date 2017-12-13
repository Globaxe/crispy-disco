# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 10:06:43 2017

@author: cedric.pahud
"""

import ply.yacc as yacc
from lex5 import tokens
import AST

operations = {
        '+' : lambda x,y: x+y,
        '-' : lambda x,y: x-y,
        '*' : lambda x,y: x*y,
        '/' : lambda x,y: x/y,
        }



precedence = (
        ('left', 'ADD_OP'),
        ('left', 'MUL_OP'),
        ('right', 'UMINUS'), #uminus n'est pas un token mais il permet de définir la précédence d'une expression
)


def p_expression_programme_statement(p):
    '''programme : statement'''
    p[0]=AST.ProgramNode(p[1])

def p_expression_programme_rec(p):
    '''programme : statement ';' programme'''
    p[0]=AST.ProgramNode([p[1]]+p[3].children)

def p_statement(p):
    '''statement : structure
    | assignation
    | PRINT expression'''
    try:
        p[0]=AST.PrintNode(p[2])
    except:
        p[0]=p[1]

def p_structure(p):
    '''structure : WHILE expression '{' programme '}' '''
    p[0]=AST.WhileNode([p[2],p[4]])

def p_assignation(p):
    '''assignation : ID '=' expression'''
    p[0]=AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_expression_num(p):
    '''expression : NUMBER
    | ID'''
    p[0]=AST.TokenNode(p[1])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
    | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2],[p[1],p[3]])

def p_expression_parenthesis(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_uminus(p):
    '''expression : ADD_OP expression %prec UMINUS'''    #%prec uminus permet de dire que ça précédence est de niveau uminus
    p[0] = AST.OpNode(p[1],[p[2]])                       #donc très grande prio dans notre liste de précédence

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

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 10:06:43 2017

@author: cedric.pahud
"""

import ply.yacc as yacc
from lex import tokens
import AST


def p_programme(p):
    '''programme : assignationBlock START NEWLINE codeBlock STOP NEWLINE'''
    p[0]=AST.ProgramNode([p[1],AST.StartNode(),p[4],AST.StopNode()])


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
    '''assignation : ID '=' expression
    | ID '=' accord'''
    p[0]=AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_setBPM(p):
    '''assignation : BPM '=' NUMBER'''
    p[0] = AST.BPMNode(AST.TokenNode(p[3]))

def p_accord(p):
    '''accord : '[' notelist ']' '''
    p[0] = AST.AccordNode(p[2])

def p_notelist(p):
    '''
    notelist : notelist ',' NOTE
    notelist : NOTE
    '''
    if len(p) == 2:
        p[0] = [AST.NoteNode(p[1])]
    else:
        p[0] = p[1]
        p[0].append(AST.NoteNode(p[3]))

def p_expression(p):
    '''expression : ID
    | SIGNAL
    | NUMBER'''
    p[0]=AST.TokenNode(p[1])

def p_statement(p):
    '''statement : repetedBlock
    | instrPlay
    | Arpegiator'''
    p[0]=p[1]

# number a la place d'expression ?
def p_repetedBlock(p):
    '''repetedBlock : REP '(' expression ')' NEWLINE '{' NEWLINE codeBlock '}' '''
    p[0]=AST.RepNode([p[3],p[8]])

# number a la place d'expression ?
# ajouter accord à expression
def p_Arpegiator(p):
    '''Arpegiator : ARP '(' expression ',' accord ',' expression ',' '+' ')'
    | ARP '(' expression ',' accord ',' expression ',' '-' ')'
    | ARP '(' expression ',' expression ',' expression ',' '+' ')'
    | ARP '(' expression ',' expression ',' expression ',' '-' ')' '''
    p[0]=AST.ArpNode([p[3],p[5],p[7],AST.SignNode(p[9])])

def p_instrPlayNote(p):
    '''instrPlay : ID NOTE'''
    p[0]=AST.PlayNode([AST.TokenNode(p[1]),AST.NoteNode(p[2])])

def p_instrPlayID(p):
    '''instrPlay : ID ID'''
    p[0]=AST.PlayNode([AST.TokenNode(p[1]),AST.TokenNode(p[2])])

def p_instrPlayAcc(p):
    '''instrPlay : ID accord'''
    p[0]=AST.PlayNode([AST.TokenNode(p[1]),p[2]])

def p_instrPause(p):
    '''instrPlay : ID PAUSE'''
    p[0]=AST.PlayNode([AST.TokenNode(p[1]),AST.PauseNode()])

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

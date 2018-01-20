import AST
import utils
from AST import addToClass

'''Valid opcodes are:

    PUSHC <val>: pushes the constant value <val> on the execution stack
    PUSHV <id>: pushes the value of the identifier <id> on the execution stack
    SET <id>: pops a value from the stack and sets <id> accordingly
    PRINT: pops a value from the stack and prints it.
    ADD, SUB, MUL, DIV: pops two values from the stack and pushes their
                sum, difference, product, quotient respectively.
    USUB: Changes the sign of the number on the top of the stack.
    JMP <tag>: jumps to <tag>
    JIZ, JINZ <tag>: if the top of the stack is (not) zero, jumps to <tag>'''

operations = {
        '+' : 'ADD',
        '-' : 'SUB',
        '*' : 'MUL',
        '/' : 'DIV',
        }


@addToClass(AST.ProgramNode)
def compile(self):
    compiled=""
    for c in self.children:
        compiled += c.compile()
    return compiled


@addToClass(AST.BPMNode)
def compile(self):
    settings.set_bpm(self.tok)

'''@addToClass(AST.TokenNode)
def compile(self):
    if isinstance(self.tok,str):
        return f"PUSHV {self.tok}\n"
    else:
        return f"PUSHC {self.tok}\n"'''


@addToClass(AST.AssignNode)
def compile(self):
    if isinstance(self.children[0].type,"token"):
        utils.addInstr(self.children[1].tok,self.children[0].tok)
    else:
        utils.addChord(self.children[1].tok,self.children[0].compile())

@addToClass(AST.AssignBlockNode)
def compile(self):
    for c in self.children:
        c.compile()
    return utils.d_starting()+utils.d_instruments()

# start node et stop node ???


'''@addToClass(AST.WhileNode)
def compile(self):
    global nbCond
    nbCond+=1
    myCond = nbCond
    compiled ="JMP cond"+str(myCond)+"\nbody"+str(myCond)+": "
    compiled+=self.children[1].compile()
    compiled+="cond"+str(myCond)+": "
    compiled+=self.children[0].compile()
    compiled+="JINZ body"+str(myCond)+"\n"
    return compiled'''

if __name__ == '__main__':
    from parser5 import parse
    import sys, os
    nbCond=0
    bytecode = ""
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    bytecode = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.vm'
    outfile = open(name,'w')
    outfile.write(bytecode)
    outfile.close()
    print("Wrote output to",name)

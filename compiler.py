import AST
import utils
from AST import addToClass


@addToClass(AST.ProgramNode)
def compile(self):
    compiled=""
    for c in self.children:
        compiled += c.compile()
    return compiled


@addToClass(AST.BPMNode)
def compile(self):
    utils.settings.set_bpm(self.children[0].tok)

@addToClass(AST.codeBlockNode)
def compile(self):
    compiled=""
    for c in self.children:
        compiled += c.compile()
    return compiled

@addToClass(AST.AssignNode)
def compile(self):
    if self.children[1].type == "token":
        utils.add_instr(self.children[0].tok,self.children[1].tok)
    elif self.children[1].type == "accord":
        utils.add_chord(self.children[0].tok,self.children[1].compile())
    elif self.children[1].type == "BPM":
        self.children[1].compile()

@addToClass(AST.AssignBlockNode)
def compile(self):
    for c in self.children:
        c.compile()
    return ""

@addToClass(AST.RepNode)
def compile(self):
    compiled = ""
    for i in range(0,self.children[0].tok):
        compiled+=self.children[1].compile()
    return compiled

@addToClass(AST.StartNode)
def compile(self):
    return utils.d_starting()+utils.d_instruments()

@addToClass(AST.StopNode)
def compile(self):
    return utils.d_end()

@addToClass(AST.AccordNode)
def compile(self):
    listNotes = []
    for c in self.children:
        listNotes.append(c.compile())
    return utils.Chord(listNotes)

@addToClass(AST.NoteNode)
def compile(self):
    return utils.Note(self.note,self.hauteur)

@addToClass(AST.PlayNode)
def compile(self):
    if self.children[1].type == "note":
        return utils.d_note(instrName=self.children[0].tok, dur=1.0, amp=10000.0, note=self.children[1].compile(), a=2.0, d=5.0, s=1.0, r=0.8, sta=1.0)
    elif self.children[1].type == "accord":
        return utils.d_chord(instrName=self.children[0].tok, dur=1.0, amp=10000.0, chord=self.children[1].compile(), a=5.0, d=20.0, s=5.0, r=2.5, sta=2.0)
    elif self.children[1].type == "token":
        return utils.d_chord(instrName=self.children[0].tok, dur=1.0, amp=10000.0, chord=self.children[1].tok, a=5.0, d=20.0, s=5.0, r=2.5, sta=2.0)

@addToClass(AST.ArpNode)
def compile(self):
    if self.children[1].type == "accord":
        return utils.d_arp(instrName=self.children[0].tok, dur=1.0, amp=10000.0, chord=self.children[1].compile(),a=5.0, d=20.0, s=5.0, r=2.5, sta=2.0,loops=self.children[2].tok)
    elif self.children[1].type == "token":
        return utils.d_arp(instrName=self.children[0].tok, dur=1.0, amp=10000.0, chord=self.children[1].tok,a=5.0, d=20.0, s=5.0, r=2.5, sta=2.0,loops=self.children[2].tok)

if __name__ == '__main__':
    from parser5 import parse
    import sys, os
    nbCond=0
    bytecode = ""
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    bytecode = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.csd'
    outfile = open(name,'w')
    outfile.write(bytecode)
    outfile.close()
    print("Wrote output to",name)

self.instruments = list()

class Instrument():
    def __init__(self, id, type):
        self.id = id
        self.type = type

def addInstr(id, type):
    instruments.append(new Instrument(id, type))

def startingDeclaration():
    return "<CsoundSynthesizer>\n<CsOptions>\n-odac\n-o out.wav _W\n</CsOptions>\n"

def instrumentsDeclaration():
    if len(instruments) != 0:
        string = "<CsInstruments>\nsr=44100\nksmps=10\nnchnls=1\n"
        for e in instruments:
            string += "instr {:d}\niamp=p4\nifreq=cpspch(p5)\niatt=p6\nidec=p7\nislev=p8\nirel=p9\nkenv adsr p3/iatt, p3/idec, islev, p3/irel\naout oscil iamp*kenv, ifreq, 1\nout aout\nendin\n".format(e.id)
        string += "<\CsInstruments>\n<CsScore>\n"
        for e in instruments:
            if e.type is "sine":
                string += "f{:d} 0 16384 10 1\n".format(e.id)
            elif e.type is "square":
                string += "f{:d} 0 16384 10 1 0 0.3 0 0.2 0 0.14 0 .111\n".format(e.id)
            elif e.type is "saw":
                string +="f{:d} 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111\n".format(e.id)
            elif e.type is "pulse":
                string +="f{:d} 0 16384 10 1 1 1 1 0.7 0.5 0.3 0.1\n"
            else:
                print("Error : Unknown instrument type\n")
    else
        print("Error : No instruments declared")
    return string

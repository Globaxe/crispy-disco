instruments = list()
noteCount = 0   

keys = {'do': "00",
         'do#': "01",
         're' : "02",
         're#' : "03",
         'mi' : '04',
         'fa' : '05',
         'fa#' : '06',
         'sol' : '07',
         'sol#' : '08',
         'la' : '09',
         'la#' : '10',
         'si' : '11'}

class Instrument():
    def __init__(self, id, type):
        self.id = id
        self.type = type

class Note():
    def __init__(self, key, octave):
        self.key = key
        self.octave = octave

class Chord():
    def __init__(self, notes):
        self.notes = notes
        

def add_instr(id, type):
    instruments.append(Instrument(id, type))

def d_starting():
    return "<CsoundSynthesizer>\n<CsOptions>\n-odac\n-o out.wav _W\n</CsOptions>\n"

def d_instruments():
    if len(instruments) != 0:
        string = "<CsInstruments>\nsr=44100\nksmps=10\nnchnls=1\n"
        for e in instruments:
            string += "instr {:d}\niamp=p4\nifreq=cpspch(p5)\niatt=p6\nidec=p7\nislev=p8\nirel=p9\nkenv adsr p3/iatt, p3/idec, islev, p3/irel\naout oscil iamp*kenv, ifreq, 1\nout aout\nendin\n".format(e.id)
        string += "</CsInstruments>\n<CsScore>\n"
        for e in instruments:
            if e.type is "sine":
                string += "f{:d} 0 16384 10 1\n".format(e.id)
            elif e.type is "square":
                string += "f{:d} 0 16384 10 1 0 0.3 0 0.2 0 0.14 0 .111\n".format(e.id)
            elif e.type is "saw":
                string +="f{:d} 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111\n".format(e.id)
            elif e.type is "pulse":
                string +="f{:d} 0 16384 10 1 1 1 1 0.7 0.5 0.3 0.1\n".format(e.id)
            else:
                print("Error : Unknown instrument type\n")
    else:
        print("Error : No instruments declared")
    return string

def d_note(instrId, dur, amp, note, a, d, s, r, sta=None):
    if sta == None:
            return "i {:d} + {:.2f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(instrId, dur, amp, note.octave, keys[note.key], a, d, s, r)
    elif sta == 0:
        return "i {:d} 0 {:.2f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(instrId, dur, amp, note.octave, keys[note.key], a, d, s, r)
    else:
        return "i {:d} ^+{:.2f} {:f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(instrId, sta, dur, amp, note.octave, keys[note.key], a, d, s, r)

def d_chord(instrId, dur, amp, chord, a, d, s, r, sta=None):
    string = ""
    for i in range(0, len(chord.notes)):
        if i == 0:
            string += d_note(instrId, dur, amp, chord.notes[i],  a, d, s, r, sta)
        else:
            string += d_note(instrId, dur, amp, chord.notes[i],  a, d, s, r)
    return string
    
        
#def d_chord(instrId, sta, dur, amp, chord, a, d, s, r):
    
def d_end():
    return "</CsScore>\n</CsoundSynthesizer>\n"

stringtest = ""

add_instr(1, 'square')
#addInstr(1, 'square')

stringtest += d_starting()
stringtest += d_instruments()
stringtest += d_note(instrId=1, dur=1.0, amp=10000.0, note=Note('la', 6), a=2.0, d=5.0, s=1.0, r=0.6, sta=0)
stringtest += d_note(instrId=1, dur=1.0, amp=10000.0, note=Note('fa',6), a=2.0, d=5.0, s=1.0, r=0.3)
stringtest += d_note(instrId=1, dur=1.0, amp=10000.0, note=Note('re', 5), a=2.0, d=5.0, s=1.0, r=0.2)
stringtest += d_note(instrId=1, dur=1.0, amp=10000.0, note=Note('la', 5), a=2.0, d=5.0, s=1.0, r=0.8)
'''
test_notes = [Note('do', 6), Note('mi', 6), Note('sol', 7)]
chord1 = Chord(test_notes)
stringtest += d_chord(instrId=1, dur=2.0, amp=10000.0, chord=chord1, a=5.0, d=20.0, s=5.0, r=2.5, sta=2.0)'''
stringtest += d_end()

with open('test.cs', 'w') as f:
    f.write(stringtest)
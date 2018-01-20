import copy

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

class Settings():
    def __init__(self):
        self.bpm = 120
        self.dt = 0.5
        
    def set_bpm(self, bpm):
        self.bpm = bpm
        self.dt = 60/self.bpm

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
            offsets.append(0)
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
    offsets[instrId-1] += dur
    print("sta", sta*settings.dt)
    print("dur", dur*settings.dt)
    if sta == None:
            return "i {:d} + {:.2f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(instrId, dur*settings.dt, amp, note.octave, keys[note.key], a, d, s, r)
    elif sta == 0:
        return "i {:d} 0 {:.2f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(instrId, dur*settings.dt, amp, note.octave, keys[note.key], a, d, s, r)
    else:
        return "i {:d} {:.2f} {:f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(instrId, sta*settings.dt, dur*settings.dt, amp, note.octave, keys[note.key], a, d, s, r)

def d_chord(instrId, dur, amp, chord, a, d, s, r, sta=None):
    string = ""
    for i in range(0, len(chord.notes)):
            string += d_note(instrId, dur, amp, chord.notes[i],  a, d, s, r, sta)
    return string

def d_arp(instrId, dur, amp, chord, a, d, s, r, loops, inc, sta = None):
    chord_cpy = copy.deepcopy(chord)
    string = ""
    offset = 0
    for i in range(loops):
        for j in range(0, len(chord_cpy.notes)):
            string += d_note(instrId, dur, amp, chord_cpy.notes[j],  a, d, s, r, sta + offset)
            offset += dur
        for k in range(len(chord_cpy.notes)):
            chord_cpy.notes[k].octave += inc
    return string
'''
def d_arp_mult(repeat, instrId, dur, amp, chord, a, d, s, r, loops, inc, sta = None):
    string = ""
    offset = 0
    for i in range(repeat):
        string += d_arp(instrId, dur, amp, chord, a, d, s, r, loops, inc, sta = None)
        offset += repeat * dur
    return string
'''
instruments = list()
offsets = list()
settings = Settings()
settings.bpm = 120
#def d_chord(instrId, sta, dur, amp, chord, a, d, s, r):

def d_end():
    return "</CsScore>\n</CsoundSynthesizer>\n"

testChord = Chord([Note('mi', 7), Note('do', 7), Note('sol', 7)])

string = ""
add_instr(1, 'saw')
add_instr(2, 'sine')
add_instr(3, 'square')
string += d_starting()
string += d_instruments()
settings.set_bpm(120)

#string += d_note(instrId=1, dur=4.0, amp=5000.0, note=Note('la', 7), a=2.0, d=5.0, s=1.0, r=2.5, sta=0)
#string += d_note(instrId=1, dur=4.0, amp=5000.0, note=Note('mi', 8), a=2.0, d=5.0, s=1.0, r=2.5, sta=0)
#string += d_note(instrId=1, dur=4.0, amp=5000.0, note=Note('mi', 8), a=2.0, d=5.0, s=1.0, r=2.5, sta=0)
#string += d_note(instrId=2, dur=4.0, amp=5000.0, note=Note('la', 8), a=2.0, d=5.0, s=1.0, r=2.5, sta=4.0)
#string += d_note(instrId=2, dur=4.0, amp=5000.0, note=Note('do', 8), a=2.0, d=5.0, s=1.0, r=2.5, sta=4.0)
string += d_note(instrId=1, dur=8.0, amp=10000.0, note=Note('la', 5), a = 3.0, d = 6.0, s = 1.0, r = 1.5, sta = 0.0)
string += d_arp(3, 0.25, 20000.0, testChord, 1.0, 1.0, 1.0, 1.0, 4, 1, 0.0)
string += d_arp(3, 0.25, 20000.0, testChord, 1.0, 1.0, 1.0, 1.0, 4, 1, 2.0)
string += d_arp(3, 0.25, 20000.0, testChord, 1.0, 1.0, 1.0, 1.0, 4, 1, 4.0)
string += d_arp(3, 0.25, 20000.0, testChord, 1.0, 1.0, 1.0, 1.0, 4, 1, 6.0)
string += d_arp(3, 0.25, 20000.0, testChord, 1.0, 1.0, 1.0, 1.0, 4, 1, 8.0)
string += d_chord(1, 5.0, 10000.0, testChord, 2.0, 5.0, 1.0, 1.0, 4.0)
string += d_end()


with open('test.cs', 'w') as f:
    f.write(string)

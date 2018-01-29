import copy
from subprocess import call

instr_id = 1
filename = ""

intstrNameId =dict()
chordsName = dict()

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
        self.offset = 0

class Note():
    def __init__(self, key, octave):
        self.key = key
        self.octave = octave

class Chord():
    def __init__(self, notes):
        self.notes = notes

def add_instr(name, type):
    global instr_id
    intstrNameId[name] = instr_id
    instruments.append(Instrument(instr_id, type))
    instr_id+=1

def add_chord(name,chord):
    chordsName[name]=chord

def d_starting():
    return f"<CsoundSynthesizer>\n<CsOptions>\n-odac\n-o {filename}.wav _W\n</CsOptions>\n"

def d_instruments():
    if len(instruments) != 0:
        string = "<CsInstruments>\nsr=44100\nksmps=10\nnchnls=1\n"
        for e in instruments:
            offsets.append(0)
            string += "instr {:d}\niamp=p4\nifreq=cpspch(p5)\niatt=p6\nidec=p7\nislev=p8\nirel=p9\nkenv adsr p3/iatt, p3/idec, islev, p3/irel\naout oscil iamp*kenv, ifreq, 1\nout aout\nendin\n".format(e.id)
        string += "</CsInstruments>\n<CsScore>\n"
        for e in instruments:
            if e.type == "sine":
                string += "f{:d} 0 16384 10 1\n".format(e.id)
            elif e.type == "square":
                string += "f{:d} 0 16384 10 1 0 0.3 0 0.2 0 0.14 0 .111\n".format(e.id)
            elif e.type == "saw":
                string +="f{:d} 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111\n".format(e.id)
            elif e.type == "pulse":
                string +="f{:d} 0 16384 10 1 1 1 1 0.7 0.5 0.3 0.1\n".format(e.id)
            else:
                print("Error : Unknown instrument type\n")
    else:
        print("Error : No instruments declared")
    return string

def d_note(instrName, dur, amp, note, a, d, s, r, sta=None, chord=False):
    if sta == None:
        if chord == False:
            instruments[intstrNameId[instrName]-1].offset += dur
        return "i {:d} {:.2f} {:.2f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(intstrNameId[instrName], instruments[intstrNameId[instrName]-1].offset * settings.dt, dur*settings.dt, amp, note.octave, keys[note.key], a, d, s, r)
    elif sta == 0:
        return "i {:d} 0 {:.2f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(intstrNameId[instrName], dur*settings.dt, amp, note.octave, keys[note.key], a, d, s, r)
    else:
        return "i {:d} {:.2f} {:f} {:.2f} {:d}.{:s} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(intstrNameId[instrName], sta*settings.dt, dur*settings.dt, amp, note.octave, keys[note.key], a, d, s, r)

def wait(instrName, dur):
    instruments[intstrNameId[instrName]].offset += dur

def d_chord(instrName, dur, amp, chord, a, d, s, r, sta=None):
    string = ""
    instruments[intstrNameId[instrName]-1].offset += dur
    if isinstance(chord,str):
        chord = chordsName[chord]
    for i in range(0, len(chord.notes)):
            string += d_note(instrName, dur, amp, chord.notes[i],  a, d, s, r, sta, chord=True)
    return string

def d_arp(instrName, dur, amp, chord, a, d, s, r, loops, inc, sta = None):
    if isinstance(chord,str):
        chord = chordsName[chord]
    chord_cpy = copy.deepcopy(chord)
    string = ""
    offset = 0
    for i in range(loops):
        for j in range(0, len(chord_cpy.notes)):
            string += d_note(instrName, dur, amp, chord_cpy.notes[j],  a, d, s, r)
            offset += dur
        for k in range(len(chord_cpy.notes)):
            chord_cpy.notes[k].octave += inc
    return string

instruments = list()
offsets = list()
settings = Settings()
# settings.bpm = 120
#def d_chord(instrId, sta, dur, amp, chord, a, d, s, r):

def d_end():
    return "</CsScore>\n</CsoundSynthesizer>\n"

if __name__ == '__main__':
    testChord = Chord([Note('mi', 7), Note('do', 7), Note('sol', 7)])

    string = ""
    add_instr('coucou', 'saw')
    string += d_starting()
    string += d_instruments()
    settings.set_bpm(120)
    string += d_note(instrName='coucou', dur=3.0, amp=10000.0, note=Note('la', 5), a = 1.0, d = 6.0, s = 1.0, r = 1.5)
    string += d_note(instrName='coucou', dur=3.0, amp=10000.0, note=Note('la', 6), a = 1.0, d = 6.0, s = 1.0, r = 1.5)
    string += d_note(instrName='coucou', dur=3.0, amp=10000.0, note=Note('la', 5), a = 1.0, d = 6.0, s = 1.0, r = 1.5)
    string += d_note(instrName='coucou', dur=3.0, amp=10000.0, note=Note('la', 6), a = 1.0, d = 6.0, s = 1.0, r = 1.5)
    string += d_chord('coucou', 3.0, 10000.0, testChord, 2.0, 5.0, 1.0, 1.0)
    string += d_arp('coucou', 1.0, 10000.0, testChord, 1.0, 1.0, 1.0, 1.0, 8, 1)
    string += d_arp('coucou', 1.0, 10000.0, testChord, 1.0, 1.0, 1.0, 1.0, 8, -1)
    string += d_end()

    with open('test.cs', 'w') as f:
        f.write(string)

    call(["csound", "test.cs"])

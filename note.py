import simpleaudio as sa
import numpy as np
import math
import json

def playNote():
    print('Note')
def getFrequencies():
    data = {}
    with open('noteFrequencies.json') as json_file:
        data = json.load(json_file)
    return data

noteFrequencies = getFrequencies()

nnotes = 12

noteNamesRelative = [
    ['A'], ['As', 'Bf'], ['B'], ['C'], ['Cs', 'Df'], 
    ['D'], ['Ds', 'Ef'], ['E'], ['F'], ['Fs', 'Gf'],
    ['G'], ['Gs', 'Af']
]

noteNamesIndex = {
    'A': 0, 'As': 1, 'Bf': 1, 'B': 2, 'C': 3, 'Cs': 4, 'Df': 4,
    'D': 5, 'Ds': 6, 'Ef': 6, 'E': 7, 'F': 8, 'Fs': 9, 'Gf': 9,
    'G': 10, 'Gs': 11, 'Af': 11
}
accidentalIndex = {
    's': 0, 'f': 1
}

def noteNameParts(noteStr):
    octInd = 1 if len(noteStr) == 2 else 2
    namePart =  noteStr[0:octInd]
    octavePart = noteStr[octInd]
    return {'name': namePart, 'octave': int(octavePart)}
'''
examples A4, Cs4 (c sharp, octave 4)
'''
class NoteString():
    def fromNoteString(self, noteStr):
        parts = noteNameParts(noteStr)
        return NoteString(parts['name'], )
    def __init__(self, note, octave):
        #parts = noteNameParts(noteStr)
        #name = parts['name']
        self.note = note+str(octave)
        self.name = note
        self.notename = note[0]
        self.accidental = note[1] if len(note) >= 2 else None
        self.octave = octave
        self.index = noteNamesIndex[note]
    def interval(self, i, useFlat=False):
        nameIndex = (self.index+i)%nnotes
        octaveChange = math.floor((self.index+i)/nnotes)
        noteNames = noteNamesRelative[nameIndex]
        ni = 1 if useFlat and len(noteNames) > 1 else 0
        newNoteString = noteNames[ni]+str(self.octave+octaveChange)
        return NoteString(newNoteString)
    def __str__(self):
        return self.note

    

def generateNotes(rm=0, rp=0, base=(NoteString('A4'), 440)):
    snote = base[0]
    sfreq = base[1]
    notes = []
    for r in range(-rm, rp+1, 1):
        note = snote.interval(r)
        nfreq = sfreq * 2 ** (r / 12)
        ntup = (note, nfreq)
        notes.append(ntup)
    return notes

def jsonFileNotes(fn, notes=[]):
    data = {str(n[0]): n[1] for n in notes}
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)

sample_rate = 44100

'''
Sine Note
'''
class Note():
    def __init__(self, ns='A4', T=0.5):
        self.time = T
        self.freq = noteFrequencies[ns]
        self.t = np.linspace(0, T, int(T*sample_rate), False)
        self.wave = np.sin(self.freq*self.t*2*np.pi)
        audio = np.hstack((self.wave))
        # normalize to 16-bit range
        audio *= 32767 / np.max(np.abs(audio))
        # convert to 16-bit data
        self.audio = audio.astype(np.int16)
    def play(self):
        # start playback
        play_obj = sa.play_buffer(self.audio, 1, 2, sample_rate)
        # wait for playback to finish before exiting
        play_obj.wait_done()

class Chord():
    def __init__(self, base=Note('A4')):
        pass

class Tempo():
    def __init__(self, tempo=60):
        self.tempo = tempo
        self.time = tempo/60
        self.t = np.linspace(0, self.time, int(self.time*sample_rate), False)
    #def     
        
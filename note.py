import simpleaudio as sa
import numpy as np
import math
import json
import re

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

sharpFlatDict = {
    'As': 'Bf', 'Bf': 'As',
    'Cs': 'Df', 'Df': 'Cs',
    'Ds': 'Ef', 'Ef': 'Ds',
    'Fs': 'Gf', 'Gf': 'Fs',
    'Gs': 'Af', 'Af': 'Gs'
}

accidentalIndex = {
    's': 0, 'f': 1
} 

#use regex
def noteNameParts(noteStr):
    parseStr = re.search('^([A-G])([sf]?)(-?[0-9]+)', noteStr)
    notename = parseStr.group(1)
    fullnote = parseStr.group(1)+parseStr.group(2)
    accidental = parseStr.group(2) if parseStr.group(2) != '' else None
    octave = int(parseStr.group(3))
    return { 
        'notename': fullnote, 'basenote': notename,
        'accidental': accidental, 'octave': octave
    }
'''
examples A4, Cs4 (c sharp, octave 4)
'''
class NoteString():
    def fromNoteString(noteStr):
        parts = noteNameParts(noteStr)
        return NoteString(parts['notename'], parts['octave'])
    def __init__(self, fullnote, octave):
        self.note = fullnote+str(octave)
        self.name = fullnote
        self.notename = fullnote[0]
        self.accidental = fullnote[1] if len(fullnote) >= 2 else None
        self.octave = octave
        self.index = noteNamesIndex[fullnote]
    def oppositeAccidental(self):
        if self.accidental != None:
            self.name = sharpFlatDict[self.name]
            self.notename = self.name[0]
            self.accidental = self.name[1]
            self.note = self.name+str(octave)
    def interval(self, i, useFlat=False):
        nameIndex = (self.index+i)%nnotes
        octaveChange = math.floor((self.index+i)/nnotes)
        noteNames = noteNamesRelative[nameIndex]
        ni = 1 if useFlat and len(noteNames) > 1 else 0
        newFullNote = noteNames[ni]
        newOctave = self.octave+octaveChange
        #newNoteString = noteNames[ni]+str(self.octave+octaveChange)
        return NoteString(newFullNote, newOctave)
    def __str__(self):
        return self.note

    

def generateNotes(rm=0, rp=0, base=(NoteString.fromNoteString('A4'), 440), sf=False):
    snote = base[0]
    sfreq = base[1]
    notes = []
    for r in range(-rm, rp+1, 1):
        note = snote.interval(r)
        nfreq = sfreq * 2 ** (r / 12)
        ntup = (note, nfreq)
        notes.append(ntup)
        #print((str(note), nfreq))
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
        
class Track():
    def __init__(self):
        pass
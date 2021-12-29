import mido
from note import generateNotes, NoteString

def openFile(f):
    mid = mido.MidiFile(f)
    return mid
'''
C-2 to A9 range (needs verification)
'''
'''
def midiNotes():
    notes = generateNotes(69, 58)
    return notes
'''
midiNotes = generateNotes(69, 58)

class Midi():
    @staticmethod
    def fromFile(fn):
        mid = mido.MidiFile(fn)
        return Midi(mid)
    def __init__(self, mid):
        self.mid = mid
        self.tracks = self.parseMidiTracks(mid)
    def parseMidiTracks(self, mid):
        tracks = []
        for i, track in enumerate(mid.tracks):
            track = [msg for msg in track]
            tracks.append(track)
        return tracks

    def getNotesTrack(self,track):
        if track < len(self.tracks):
            for msg in self.tracks[track]:
                if msg.type == 'note_on' or msg.type=='note_off':
                    print(msg)
                    #print(midiNotes[msg.note][0])

    def getMsg(self, track):
        if track < len(self.tracks):
            return self.tracks[track]
        return []

class MidiTrack():
    def __init__(self, track):
        pass
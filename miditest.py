import midideco

midi = midideco.Midi.fromFile('Trainer_Battle_Pokemon_Red-Blue_Yellow_OST_002.mid')

tracks = midi.tracks

#print(midi.getMsg(0))
midi.getNotesTrack(2)


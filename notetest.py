import note

ns = note.NoteString('A4')

notes = note.generateNotes(24, 36)
note.jsonFileNotes('noteFrequencies.json', notes)

note.Note('C2').play()
note.Note('C3').play()

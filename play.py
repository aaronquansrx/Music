import numpy as np
import simpleaudio as sa

import matplotlib.pylab as plt

def chrom_scale(freq, time=0.1, sample_rate=44100):
    t = np.linspace(0, time, int(time*sample_rate), False)
    tup = tuple((np.sin((freq * 2 ** (i/12)) * t * 2 * np.pi) for i in range(12)))

    return tup

# calculate note frequencies
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)

# get timesteps for each sample, T is note duration in seconds
sample_rate = 44100
T = 1
t = np.linspace(0, T, int(T * sample_rate), False)

# generate sine wave notes
A_note = np.sin(A_freq * t * 2 * np.pi)
Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
E_note = np.sin(E_freq * t * 2 * np.pi)
chord = [A_note, Csh_note, E_note]

third = np.add.reduce(chord)

chrom = chrom_scale(A_freq, 0.5)
audio = np.hstack(third)

# concatenate notes
#audio = np.hstack((A_note, Csh_note, E_note))
# normalize to 16-bit range
audio *= 32767 / np.max(np.abs(audio))
# convert to 16-bit data
audio = audio.astype(np.int16)

# start playback
play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

'''
t3 = np.linspace(0, 0.5, int(0.5 * sample_rate)*12, False)
plt.plot(t3, audio)
plt.show()
'''


# wait for playback to finish before exiting
play_obj.wait_done()


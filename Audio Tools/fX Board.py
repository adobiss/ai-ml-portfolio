import soundfile as sf
from pedalboard import (
    Pedalboard,
    Convolution,
    Compressor,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    LadderFilter,
    Phaser,
)

audio, sample_rate = sf.read(r'C:\Users\AD\Downloads\You Tell Me.wav')

sr = sample_rate

# Make a Pedalboard object, containing multiple plugins:
board = Pedalboard([
    Compressor(threshold_db=-50, ratio=25),
    Gain(gain_db=30),
    Chorus(),
    LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
    Phaser(),
    #Convolution("./guitar_amp.wav", 1.0),
    Reverb(room_size=0.25),
], sample_rate=sr)

# Pedalboard objects behave like lists, so you can add plugins:
board.append(Compressor(threshold_db=-25, ratio=10))
board.append(Gain(gain_db=10))
board.append(Limiter())

# Run the audio through this pedalboard!
effected = board(audio)

# Write the audio back as a wav file:
with sf.SoundFile('./processed-output-stereo.wav', 'w', samplerate=sr, channels=effected.shape[1]) as f:
    f.write(effected)
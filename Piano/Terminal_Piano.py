import numpy as np
import pygame
import sys

# Initialize audio mixer
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

def generate_tone(frequency, duration=1.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.7 * np.sin(2 * np.pi * frequency * t) + 0.3 * np.sin(4 * np.pi * frequency * t)
    envelope = np.exp(-3.0 * t)
    audio = (wave * envelope * 32767).astype(np.int16)
    
    # Reshape to 2D for pygame stereo compatibility ([samples, channels])
    audio = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(audio)

KEY_NOTE_MAP = {
    'a': ('C4', 0),   'w': ('C#4', 1), 's': ('D4', 2),  'e': ('D#4', 3),
    'd': ('E4', 4),   'f': ('F4', 5),  't': ('F#4', 6), 'g': ('G4', 7),
    'y': ('G#4', 8),  'h': ('A4', 9),  'u': ('A#4', 10),'j': ('B4', 11),
    'k': ('C5', 12)
}

MIDDLE_C_FREQ = 261.63
sounds = {}
for key, (name, semitone) in KEY_NOTE_MAP.items():
    freq = MIDDLE_C_FREQ * (2 ** (semitone / 12.0))
    sounds[key] = (name, generate_tone(freq))

print("--- Terminal Piano ---")
print("Press keys [A-K] for white keys, [W, E, T, Y, U] for black keys. Press ESC to quit.")

screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("Terminal Keyboard Focus")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            char = event.unicode.lower()
            if char in sounds:
                note_name, sound = sounds[char]
                sound.play()
                print(f"Played Note: {note_name} (Key: '{char.upper()}')")

pygame.quit()
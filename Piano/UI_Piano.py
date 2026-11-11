import tkinter as tk
import numpy as np
import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

def generate_tone(frequency, duration=1.8, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.75 * np.sin(2 * np.pi * frequency * t) + 0.25 * np.sin(4 * np.pi * frequency * t)
    envelope = np.exp(-2.8 * t)
    audio = (wave * envelope * 32767).astype(np.int16)
    
    # Reshape to 2D for stereo mixer
    audio = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(audio)

MIDDLE_C_FREQ = 261.63

KEY_MAPPINGS = {
    'a': ('C4', 0, 'white'),   'w': ('C#4', 1, 'black'),
    's': ('D4', 2, 'white'),   'e': ('D#4', 3, 'black'),
    'd': ('E4', 4, 'white'),
    'f': ('F4', 5, 'white'),   't': ('F#4', 6, 'black'),
    'g': ('G4', 7, 'white'),   'y': ('G#4', 8, 'black'),
    'h': ('A4', 9, 'white'),   'u': ('A#4', 10, 'black'),
    'j': ('B4', 11, 'white'),
    'k': ('C5', 12, 'white')
}

class TkinterPiano(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Tkinter Synthesizer")
        self.geometry("620x360")  # Fixed geometry string without spaces
        self.config(bg="#1e1e1e")
        self.resizable(False, False)

        self.sounds = {}
        for char, (name, semitone, ktype) in KEY_MAPPINGS.items():
            freq = MIDDLE_C_FREQ * (2 ** (semitone / 12.0))
            self.sounds[char] = {
                'name': name,
                'sound': generate_tone(freq),
                'type': ktype
            }

        self.setup_ui()
        self.draw_keyboard()

        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)

        self.pressed_keys = set()

    def setup_ui(self):
        title_label = tk.Label(
            self, text="Tkinter Synthesizer", 
            font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#1e1e1e"
        )
        title_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#1e1e1e")
        btn_frame.pack(pady=5)

        play_btn = tk.Button(
            btn_frame, text="▶ Play 'Ode to Joy'", 
            font=("Helvetica", 10, "bold"), bg="#2d89ef", fg="white", 
            activebackground="#006bc7", activeforeground="white",
            command=self.play_ode_to_joy, relief="flat", padx=10, pady=5
        )
        play_btn.pack()

        self.canvas = tk.Canvas(self, width=560, height=200, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=15)

    def draw_keyboard(self):
        self.key_rects = {}
        white_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k']
        w_width, w_height = 65, 180
        
        for idx, char in enumerate(white_keys):
            x1 = 20 + idx * (w_width + 4)
            y1 = 10
            x2 = x1 + w_width
            y2 = y1 + w_height

            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFFFF", outline="#000000", width=2)
            self.canvas.create_text(x1 + w_width / 2, y2 - 20, text=f"{self.sounds[char]['name']}\n({char.upper()})", fill="#333333", font=("Helvetica", 9, "bold"))
            self.key_rects[char] = (rect, "#FFFFFF")

        black_key_positions = {
            'w': 0, 'e': 1, 't': 3, 'y': 4, 'u': 5
        }
        b_width, b_height = 40, 110
        for char, pos in black_key_positions.items():
            x1 = 20 + (pos + 1) * (w_width + 4) - (b_width / 2) - 2
            y1 = 10
            x2 = x1 + b_width
            y2 = y1 + b_height

            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#222222", outline="#000000", width=2)
            self.canvas.create_text(x1 + b_width / 2, y2 - 15, text=char.upper(), fill="#FFFFFF", font=("Helvetica", 8, "bold"))
            self.key_rects[char] = (rect, "#222222")

    def trigger_note(self, char):
        if char in self.sounds:
            self.sounds[char]['sound'].play()
            rect, _ = self.key_rects[char]
            self.canvas.itemconfig(rect, fill="#4CAF50")

    def release_note(self, char):
        if char in self.key_rects:
            rect, orig_color = self.key_rects[char]
            self.canvas.itemconfig(rect, fill=orig_color)

    def on_key_press(self, event):
        char = event.char.lower()
        if char in self.sounds and char not in self.pressed_keys:
            self.pressed_keys.add(char)
            self.trigger_note(char)

    def on_key_release(self, event):
        char = event.char.lower()
        if char in self.pressed_keys:
            self.pressed_keys.remove(char)
            self.release_note(char)

    def play_ode_to_joy(self):
        melody = [
            ('d', 400), ('d', 400), ('f', 400), ('g', 400),
            ('g', 400), ('f', 400), ('d', 400), ('s', 400),
            ('a', 400), ('a', 400), ('s', 400), ('d', 400),
            ('d', 600), ('s', 200), ('s', 800),

            ('d', 400), ('d', 400), ('f', 400), ('g', 400),
            ('g', 400), ('f', 400), ('d', 400), ('s', 400),
            ('a', 400), ('a', 400), ('s', 400), ('d', 400),
            ('s', 600), ('a', 200), ('a', 800)
        ]

        def step(index):
            if index < len(melody):
                char, delay = melody[index]
                self.trigger_note(char)
                self.after(300, lambda: self.release_note(char))
                self.after(delay, lambda: step(index + 1))

        step(0)

if __name__ == "__main__":
    app = TkinterPiano()
    app.mainloop()
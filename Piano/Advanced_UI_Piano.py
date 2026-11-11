import tkinter as tk
from tkinter import ttk
import numpy as np
import pygame

# Initialize Pygame sound engine
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

MIDDLE_C_FREQ = 261.63

# Extended Key Mappings (Two Octaves: C4 to C5 + extra)
# Format: key_char: (Note Name, Semitone Offset, Key Type, PC Keyboard Key label)
KEY_CONFIGS = [
    ('z', 'C4', 0, 'white'),   ('s', 'C#4', 1, 'black'),
    ('x', 'D4', 2, 'white'),   ('d', 'D#4', 3, 'black'),
    ('c', 'E4', 4, 'white'),
    ('v', 'F4', 5, 'white'),   ('g', 'F#4', 6, 'black'),
    ('b', 'G4', 7, 'white'),   ('h', 'G#4', 8, 'black'),
    ('n', 'A4', 9, 'white'),   ('j', 'A#4', 10, 'black'),
    ('m', 'B4', 11, 'white'),
    (',', 'C5', 12, 'white'),  ('l', 'C#5', 13, 'black'),
    ('.', 'D5', 14, 'white'),  (';', 'D#5', 15, 'black'),
    ('/', 'E5', 16, 'white')
]

class AdvancedTkinterPiano(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yamaha-Style Python Synthesizer & Mixer")
        self.geometry("825x460")
        self.config(bg="#121212")
        self.resizable(False, False)

        # Mixer Control Variables
        self.volume_var = tk.DoubleVar(value=0.7)
        self.decay_var = tk.DoubleVar(value=2.5)
        self.harmonic_var = tk.DoubleVar(value=0.3)

        self.setup_ui()
        self.build_keyboard_layout()

        # Keyboard bindings
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)
        self.pressed_keys = set()

    def setup_ui(self):
        # Header Title
        title_frame = tk.Frame(self, bg="#121212")
        title_frame.pack(pady=10)
        tk.Label(
            title_frame, text="🎹 Python Synth Workstation", 
            font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#121212"
        ).pack()

        # Mixer Panel Frame
        mixer_frame = tk.LabelFrame(
            self, text=" Audio Mixer & Controls ", 
            font=("Helvetica", 10, "bold"), fg="#00bcd4", bg="#1e1e1e", bd=2, relief="groove"
        )
        mixer_frame.pack(fill="x", padx=20, pady=5)

        # Sliders grid inside mixer panel
        controls_container = tk.Frame(mixer_frame, bg="#1e1e1e")
        controls_container.pack(padx=10, pady=8, fill="x")

        # 1. Volume Slider
        vol_frame = tk.Frame(controls_container, bg="#1e1e1e")
        vol_frame.pack(side="left", expand=True)
        tk.Label(vol_frame, text="Volume", fg="white", bg="#1e1e1e", font=("Helvetica", 9)).pack()
        tk.Scale(vol_frame, variable=self.volume_var, from_=0.0, to=1.0, resolution=0.05, orient="horizontal", bg="#1e1e1e", fg="white", highlightthickness=0, length=140).pack()

        # 2. Decay / Sustain Slider
        decay_frame = tk.Frame(controls_container, bg="#1e1e1e")
        decay_frame.pack(side="left", expand=True)
        tk.Label(decay_frame, text="Sustain / Decay", fg="white", bg="#1e1e1e", font=("Helvetica", 9)).pack()
        tk.Scale(decay_frame, variable=self.decay_var, from_=1.0, to=5.0, resolution=0.1, orient="horizontal", bg="#1e1e1e", fg="white", highlightthickness=0, length=140).pack()

        # 3. Harmonic Mix Slider
        harm_frame = tk.Frame(controls_container, bg="#1e1e1e")
        harm_frame.pack(side="left", expand=True)
        tk.Label(harm_frame, text="Overtone Richness", fg="white", bg="#1e1e1e", font=("Helvetica", 9)).pack()
        tk.Scale(harm_frame, variable=self.harmonic_var, from_=0.0, to=0.8, resolution=0.05, orient="horizontal", bg="#1e1e1e", fg="white", highlightthickness=0, length=140).pack()

        # Demo Button Frame
        btn_frame = tk.Frame(self, bg="#121212")
        btn_frame.pack(pady=5)
        tk.Button(
            btn_frame, text="▶ Play 'Ode to Joy' Demo", 
            font=("Helvetica", 10, "bold"), bg="#00bcd4", fg="#121212", 
            activebackground="#008394", activeforeground="white",
            command=self.play_ode_to_joy, relief="flat", padx=12, pady=4
        ).pack()

        # Piano Canvas
        self.canvas = tk.Canvas(self, width=785, height=210, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=10)

    def generate_tone(self, frequency):
        sample_rate = 44100
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Mix fundamental sine wave with harmonic overtone based on mixer slider
        harm_mix = self.harmonic_var.get()
        wave = (1.0 - harm_mix) * np.sin(2 * np.pi * frequency * t) + harm_mix * np.sin(4 * np.pi * frequency * t)
        
        # Apply exponential decay envelope modified by sustain slider
        decay_rate = self.decay_var.get()
        envelope = np.exp(-decay_rate * t)
        
        # Scale by volume setting
        volume = self.volume_var.get()
        audio = (wave * envelope * 32767 * volume).astype(np.int16)
        
        # Convert to stereo format required by Pygame
        audio = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(audio)

    def build_keyboard_layout(self):
        self.key_elements = {}
        
        w_width, w_height = 70, 190
        b_width, b_height = 40, 115
        
        white_keys_data = [item for item in KEY_CONFIGS if item[3] == 'white']
        black_keys_data = [item for item in KEY_CONFIGS if item[3] == 'black']

        # 1. Render White Keys First
        for idx, (char, name, semitone, _) in enumerate(white_keys_data):
            x1 = 15 + idx * (w_width + 3)
            y1 = 10
            x2 = x1 + w_width
            y2 = y1 + w_height

            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFFFF", outline="#333333", width=2)
            self.canvas.create_text(x1 + w_width / 2, y2 - 25, text=name, fill="#333333", font=("Helvetica", 9, "bold"))
            self.canvas.create_text(x1 + w_width / 2, y2 - 10, text=f"[{char.upper()}]", fill="#777777", font=("Helvetica", 8))

            # Bind mouse click events
            self.canvas.tag_bind(rect, "<Button-1>", lambda e, c=char: self.on_mouse_click(c))
            
            freq = MIDDLE_C_FREQ * (2 ** (semitone / 12.0))
            self.key_elements[char] = {
                'rect': rect, 'orig_color': "#FFFFFF", 'freq': freq, 'name': name
            }

        # 2. Render Black Keys Over White Keys
        # Positions relative to white key indices
        black_key_offsets = {
            's': 0, 'd': 1, 'g': 3, 'h': 4, 'j': 5, 'l': 7, ';': 8
        }
        
        for char, name, semitone, _ in black_keys_data:
            # Find matching white key base position index
            white_idx = 0
            if char == 's': white_idx = 0
            elif char == 'd': white_idx = 1
            elif char == 'g': white_idx = 3
            elif char == 'h': white_idx = 4
            elif char == 'j': white_idx = 5
            elif char == 'l': white_idx = 7
            elif char == ';': white_idx = 8

            x1 = 15 + (white_idx + 1) * (w_width + 3) - (b_width / 2) - 1
            y1 = 10
            x2 = x1 + b_width
            y2 = y1 + b_height

            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#222222", outline="#000000", width=2)
            self.canvas.create_text(x1 + b_width / 2, y2 - 30, text=name, fill="#FFFFFF", font=("Helvetica", 8, "bold"))
            self.canvas.create_text(x1 + b_width / 2, y2 - 15, text=char.upper(), fill="#AAAAAA", font=("Helvetica", 7, "bold"))

            # Bind mouse click events
            self.canvas.tag_bind(rect, "<Button-1>", lambda e, c=char: self.on_mouse_click(c))

            freq = MIDDLE_C_FREQ * (2 ** (semitone / 12.0))
            self.key_elements[char] = {
                'rect': rect, 'orig_color': "#222222", 'freq': freq, 'name': name
            }

    def trigger_note(self, char):
        if char in self.key_elements:
            data = self.key_elements[char]
            sound = self.generate_tone(data['freq'])
            sound.play()
            
            # Light up key color
            self.canvas.itemconfig(data['rect'], fill="#00bcd4")
            self.after(250, lambda: self.canvas.itemconfig(data['rect'], fill=data['orig_color']))

    def on_mouse_click(self, char):
        self.trigger_note(char)

    def on_key_press(self, event):
        char = event.char.lower()
        if char in self.key_elements and char not in self.pressed_keys:
            self.pressed_keys.add(char)
            self.trigger_note(char)

    def on_key_release(self, event):
        char = event.char.lower()
        if char in self.pressed_keys:
            self.pressed_keys.remove(char)

    def play_ode_to_joy(self):
        melody = [
            ('c', 350), ('c', 350), ('v', 350), ('b', 350),
            ('b', 350), ('v', 350), ('c', 350), ('x', 350),
            ('n', 350), ('n', 350), ('x', 350), ('c', 350),
            ('c', 500), ('x', 200), ('x', 700)
        ]

        def step(index):
            if index < len(melody):
                char, delay = melody[index]
                self.trigger_note(char)
                self.after(delay, lambda: step(index + 1))

        step(0)

if __name__ == "__main__":
    app = AdvancedTkinterPiano()
    app.mainloop()
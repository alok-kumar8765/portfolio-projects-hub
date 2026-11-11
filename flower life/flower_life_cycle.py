import pygame
import numpy as np
import sys
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Life of a Flower 🌸")
clock = pygame.time.Clock()

# Colors (RGB)
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (220, 240, 255)
SOIL_COLOR = (101, 67, 33)
STEM_COLOR = (46, 139, 87)
LEAF_COLOR = (60, 179, 113)

class FlowerLifeCycle:
    def __init__(self):
        # Life cycle phases (in seconds)
        self.phase_durations = {
            "seed": 2.0,
            "grow": 3.0,
            "bloom": 4.0,
            "wilt": 3.0
        }
        self.total_cycle = sum(self.phase_durations.values())
        self.time_elapsed = 0.0
        
        # Particles for falling seeds/petals
        self.particles = []

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed >= self.total_cycle:
            self.time_elapsed = 0.0
            self.particles.clear()

    def get_current_phase(self):
        t = self.time_elapsed
        cum = 0
        for phase, duration in self.phase_durations.items():
            cum += duration
            if t <= cum:
                # Return phase name and local progress (0.0 to 1.0)
                local_t = (t - (cum - duration)) / duration
                return phase, local_t
        return "wilt", 1.0

    def draw(self, surface):
        # 1. Draw Background Sky and Soil
        for y in range(HEIGHT - 150):
            factor = y / (HEIGHT - 150)
            color = (
                int(SKY_TOP[0] * (1 - factor) + SKY_BOTTOM[0] * factor),
                int(SKY_TOP[1] * (1 - factor) + SKY_BOTTOM[1] * factor),
                int(SKY_TOP[2] * (1 - factor) + SKY_BOTTOM[2] * factor)
            )
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))
            
        pygame.draw.rect(surface, SOIL_COLOR, (0, HEIGHT - 150, WIDTH, 150))
        pygame.draw.line(surface, (70, 45, 20), (0, HEIGHT - 150), (WIDTH, HEIGHT - 150), 4)

        phase, progress = self.get_current_phase()
        stem_base_x, stem_base_y = WIDTH // 2, HEIGHT - 150

        # --- PHASE 1: SEED ---
        if phase == "seed":
            # Seed rests on soil
            seed_y = stem_base_y + int(10 * (1 - progress))
            pygame.draw.ellipse(surface, (80, 50, 20), (stem_base_x - 8, seed_y, 16, 10))

        # --- PHASE 2: GROW (Sprout & Stem) ---
        elif phase == "grow":
            # Stem height grows using ease-out curve
            max_height = 220
            current_height = max_height * np.sin(progress * np.pi / 2)
            stem_top_y = stem_base_y - current_height

            # Draw stem
            pygame.draw.line(surface, STEM_COLOR, (stem_base_x, stem_base_y), (stem_base_x, stem_top_y), 6)

            # Leaves unfurl halfway up
            if progress > 0.4:
                leaf_prog = (progress - 0.4) / 0.6
                leaf_w = int(40 * leaf_prog)
                # Left leaf
                pygame.draw.ellipse(surface, LEAF_COLOR, (stem_base_x - leaf_w, stem_base_y - 100, leaf_w, 15))
                # Right leaf
                pygame.draw.ellipse(surface, LEAF_COLOR, (stem_base_x, stem_base_y - 120, leaf_w, 15))

        # --- PHASE 3: BLOOM ---
        elif phase == "bloom":
            max_height = 220
            stem_top_y = stem_base_y - max_height
            pygame.draw.line(surface, STEM_COLOR, (stem_base_x, stem_base_y), (stem_base_x, stem_top_y), 6)
            
            # Leaves
            pygame.draw.ellipse(surface, LEAF_COLOR, (stem_base_x - 40, stem_base_y - 100, 40, 15))
            pygame.draw.ellipse(surface, LEAF_COLOR, (stem_base_x, stem_base_y - 120, 40, 15))

            # Petals expand smoothly
            petal_scale = np.sin(progress * np.pi / 2) * 55
            num_petals = 8
            
            # Draw petals in a circle
            for i in range(num_petals):
                angle = i * (2 * math.pi / num_petals)
                px = stem_base_x + int(math.cos(angle) * petal_scale)
                py = stem_top_y + int(math.sin(angle) * petal_scale)
                pygame.draw.circle(surface, (255, 105, 180), (px, py), 25)

            # Center core
            pygame.draw.circle(surface, (255, 215, 0), (stem_base_x, stem_top_y), 18)

        # --- PHASE 4: WILT ---
        elif phase == "wilt":
            max_height = 220
            # Stem droops to the side
            droop_offset = int(40 * progress)
            stem_top_y = (stem_base_y - max_height) + int(30 * progress)
            
            pygame.draw.line(surface, STEM_COLOR, (stem_base_x, stem_base_y), (stem_base_x + droop_offset, stem_top_y), 6)

            # Fading/browning petals and dropping particles
            petal_scale = 55
            num_petals = 8
            
            # Color shifts from pink to brownish-yellow
            r = int(255 - (55 * progress))
            g = int(105 + (50 * progress))
            b = int(180 - (120 * progress))
            wilt_color = (max(0, r), max(0, g), max(0, b))

            for i in range(num_petals):
                angle = i * (2 * math.pi / num_petals) + (progress * 0.5) # droop rotation
                px = stem_base_x + droop_offset + int(math.cos(angle) * (petal_scale * (1 - 0.2 * progress)))
                py = stem_top_y + int(math.sin(angle) * (petal_scale * (1 - 0.2 * progress))) + int(40 * progress) # sagging down
                
                # Drop petals off towards the end of wilt
                if progress > 0.7 and i % 2 == 0:
                    py += int(100 * (progress - 0.7)) # fall to ground
                
                pygame.draw.circle(surface, wilt_color, (px, py), int(25 * (1 - 0.3 * progress)))

            # Center core turning brown
            pygame.draw.circle(surface, (139, 69, 19), (stem_base_x + droop_offset, stem_top_y), 16)

        # UI Text Indicator
        font = pygame.font.SysFont("Helvetica", 24, bold=True)
        text_surface = font.render(f"Phase: {phase.upper()} ({int(self.time_elapsed)}s / {int(self.total_cycle)}s)", True, (50, 50, 50))
        surface.blit(text_surface, (20, 20))


def main():
    sim = FlowerLifeCycle()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0 # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.update(dt)
        sim.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
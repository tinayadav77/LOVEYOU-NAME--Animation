import pygame
import math

# --- SETTINGS ---
WIDTH = 1000
HEIGHT = 600

BACKGROUND = (0, 0, 0)
PARTICLE_COLOR = (255, 60, 80)

PARTICLE_TEXT = "LOVE YOU"

PARTICLE_FONT_SIZE = 7
LETTER_FONT_SIZE = 170

PARTICLES_PER_SECOND = 7
MOVEMENT_SPEED = 0.05

# Space between letters
LETTER_GAP = 65

# Distance between particle positions
SAMPLE_GAP = 7



pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LOVE YOU → TINA")

clock = pygame.time.Clock()

# Fonts
big_font = pygame.font.SysFont(
    "arial",
    LETTER_FONT_SIZE,
    bold=True
)

particle_font = pygame.font.SysFont(
    "arial",
    PARTICLE_FONT_SIZE,
    bold=True
)



# CREATE LETTER TARGETS
letters = ["T", "I", "N", "A"]

letter_targets = []

# Calculate total width manually
letter_widths = []

for letter in letters:
    temp_surface = big_font.render(
        letter,
        True,
        (255, 255, 255)
    )
    letter_widths.append(temp_surface.get_width())


total_width = sum(letter_widths) + LETTER_GAP * 3

start_x = (WIDTH - total_width) // 2

current_x = start_x



# CREATE TARGET POSITIONS FOR EACH LETTER


for letter_index, letter in enumerate(letters):

    # Render one letter
    text_surface = big_font.render(
        letter,
        True,
        (255, 255, 255)
    )

    letter_width = text_surface.get_width()
    letter_height = text_surface.get_height()

    # Position the letter
    letter_x = current_x
    letter_y = (HEIGHT - letter_height) // 2

    targets = []

    for y in range(0, letter_height, SAMPLE_GAP):

        for x in range(0, letter_width, SAMPLE_GAP):

            pixel = text_surface.get_at((x, y))

            if pixel.a > 0:

                target_x = letter_x + x
                target_y = letter_y + y

                targets.append(
                    (target_x, target_y)
                )

    letter_targets.append(targets)

    # Move to next letter
    current_x += letter_width + LETTER_GAP


# PARTICLE CLASS

class Particle:

    def __init__(self, target_x, target_y, start_x, start_y):

        self.x = start_x
        self.y = start_y

        self.target_x = target_x
        self.target_y = target_y

        self.finished = False

    def update(self):

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        self.x += dx * MOVEMENT_SPEED
        self.y += dy * MOVEMENT_SPEED

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 1:

            self.x = self.target_x
            self.y = self.target_y

            self.finished = True

    def draw(self):

        particle = particle_font.render(
            PARTICLE_TEXT,
            True,
            PARTICLE_COLOR
        )

        rect = particle.get_rect(
            center=(int(self.x), int(self.y))
        )

        screen.blit(particle, rect)



# ANIMATION VARIABLES

particles = []

current_letter = 0
next_particle = 0

spawn_timer = 0

animation_finished = False



# MAIN LOOP

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    if not animation_finished:

        # Make sure there are still letters left
        if current_letter < len(letter_targets):

            current_targets = letter_targets[current_letter]

            spawn_timer += clock.get_time()

            # SPAWN PARTICLES FOR CURRENT LETTER
            
            if (
                spawn_timer >= 1000 / PARTICLES_PER_SECOND
                and next_particle < len(current_targets)
            ):

                target_x, target_y = current_targets[next_particle]

                # STARTING POINT
                # Start from the BOTTOM of
                # the current letter.
                
                root_x = current_targets[len(current_targets) // 2][0]
                root_y = HEIGHT + 20

                start_x = root_x
                start_y = root_y
                particles.append(
                    Particle(
                        target_x,
                        target_y,
                        start_x,
                        start_y
                    )
                )

                next_particle += 1

                spawn_timer = 0

            # MOVE PARTICLES
            for particle in particles:
                particle.update()

            # CURRENT LETTER COMPLETED?
        
            if (
                next_particle == len(current_targets)
                and all(
                    particle.finished
                    for particle in particles
                )
            ):

                # Move to next letter
                current_letter += 1

                next_particle = 0

                spawn_timer = 0


                # If all four letters are complete
                if current_letter >= len(letter_targets):

                    animation_finished = True


    screen.fill(BACKGROUND)

    for particle in particles:
        particle.draw()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()

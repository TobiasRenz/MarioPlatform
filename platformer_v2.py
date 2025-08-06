import pygame
import sys
import random
import numpy as np

pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=128)
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_GREEN = (0, 128, 0)
LIGHT_BROWN = (205, 133, 63)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

def generate_tone(frequency, duration, sample_rate=22050):
    """Generate a simple tone for retro-style music"""
    frames = int(duration * sample_rate)
    arr = np.zeros(frames)
    
    for i in range(frames):
        # Square wave for retro sound
        arr[i] = 0.15 * np.sign(np.sin(2 * np.pi * frequency * i / sample_rate))
    
    # Fade in/out to prevent clicks
    fade_frames = frames // 20
    for i in range(fade_frames):
        arr[i] *= i / fade_frames
        arr[frames - 1 - i] *= i / fade_frames
    
    return arr

def create_background_music():
    """Create retro-style background music"""
    sample_rate = 22050
    
    # Simple melody notes (frequencies in Hz)
    notes = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
        'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99
    }
    
    # Simple Mario-inspired melody pattern (slower tempo)
    melody = [
        ('E5', 0.3), ('E5', 0.3), ('E5', 0.6), ('C5', 0.3), ('E5', 0.6),
        ('G5', 0.9), ('G4', 0.9),
        ('C5', 0.6), ('G4', 0.6), ('E4', 0.9),
        ('A4', 0.6), ('B4', 0.6), ('A4', 0.6), ('G4', 0.9),
        ('E5', 0.6), ('G5', 0.6), ('A5', 0.9), ('F5', 0.3), ('G5', 0.6),
        ('E5', 0.6), ('C5', 0.3), ('D5', 0.3), ('B4', 0.9)
    ]
    
    # Generate the music
    music_data = np.array([])
    for note, duration in melody:
        if note in notes:
            tone = generate_tone(notes[note], duration)
            music_data = np.concatenate([music_data, tone])
    
    # Convert to pygame sound format
    music_data = (music_data * 32767).astype(np.int16)
    stereo_data = np.column_stack((music_data, music_data))
    
    return pygame.sndarray.make_sound(stereo_data)

def create_jump_sound():
    """Create a jump sound effect"""
    sample_rate = 22050
    duration = 0.2
    
    # Rising pitch for jump effect
    start_freq = 300
    end_freq = 600
    
    frames = int(duration * sample_rate)
    sound_data = np.zeros(frames)
    
    for i in range(frames):
        # Frequency sweeps upward
        freq = start_freq + (end_freq - start_freq) * (i / frames)
        sound_data[i] = 1.5 * np.sin(2 * np.pi * freq * i / sample_rate)
        
        # Fade out
        sound_data[i] *= (1 - i / frames)
    
    sound_data = (sound_data * 32767).astype(np.int16)
    stereo_data = np.column_stack((sound_data, sound_data))
    return pygame.sndarray.make_sound(stereo_data)

def create_coin_sound():
    """Create a coin collection sound effect"""
    sample_rate = 22050
    duration = 0.4
    
    # Bright, happy sound for coin collection
    frequencies = [659.25, 783.99, 1046.50]  # E5, G5, C6
    
    frames = int(duration * sample_rate)
    sound_data = np.zeros(frames)
    
    for i, freq in enumerate(frequencies):
        start_frame = i * frames // len(frequencies)
        end_frame = (i + 1) * frames // len(frequencies)
        
        for j in range(start_frame, end_frame):
            sound_data[j] = 1.2 * np.sin(2 * np.pi * freq * j / sample_rate)
            # Fade each note
            note_progress = (j - start_frame) / (end_frame - start_frame)
            sound_data[j] *= (1 - note_progress * 0.3)  # Less aggressive fade
    
    sound_data = (sound_data * 32767).astype(np.int16)
    stereo_data = np.column_stack((sound_data, sound_data))
    return pygame.sndarray.make_sound(stereo_data)

def create_death_sound():
    """Create a death sound effect"""
    sample_rate = 22050
    duration = 0.6
    
    # Descending pitch for death effect
    start_freq = 500
    end_freq = 80
    
    frames = int(duration * sample_rate)
    sound_data = np.zeros(frames)
    
    for i in range(frames):
        # Frequency sweeps downward
        freq = start_freq + (end_freq - start_freq) * (i / frames)
        sound_data[i] = 1.5 * np.sin(2 * np.pi * freq * i / sample_rate)
        
        # Fade out slowly
        sound_data[i] *= (1 - i / frames) * 0.9
    
    sound_data = (sound_data * 32767).astype(np.int16)
    stereo_data = np.column_stack((sound_data, sound_data))
    return pygame.sndarray.make_sound(stereo_data)

def create_enemy_defeat_sound():
    """Create a success sound for defeating enemies"""
    sample_rate = 22050
    duration = 0.4
    
    # Ascending notes for success feeling
    frequencies = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    
    frames = int(duration * sample_rate)
    sound_data = np.zeros(frames)
    
    for i, freq in enumerate(frequencies):
        start_frame = i * frames // len(frequencies)
        end_frame = (i + 1) * frames // len(frequencies)
        
        for j in range(start_frame, end_frame):
            sound_data[j] = 1.0 * np.sin(2 * np.pi * freq * j / sample_rate)
            # Fade each note
            note_progress = (j - start_frame) / (end_frame - start_frame)
            sound_data[j] *= (1 - note_progress * 0.2)  # Gentle fade
    
    sound_data = (sound_data * 32767).astype(np.int16)
    stereo_data = np.column_stack((sound_data, sound_data))
    return pygame.sndarray.make_sound(stereo_data)

class Player:
    def __init__(self, x, y, jump_sound=None):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.jump_sound = jump_sound
        self.jump_key_pressed = False
        self.respawn_timer = 0
        self.is_dead = False
    
    def update(self, platforms):
        # Handle respawn timer
        if self.is_dead:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_dead = False
                self.x = 100
                self.y = 100
                self.vel_x = 0
                self.vel_y = 0
            return None
        
        keys = pygame.key.get_pressed()
        
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        
        jump_key_down = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        
        if jump_key_down and not self.jump_key_pressed and self.on_ground:
            # Play sound IMMEDIATELY when key is pressed
            if self.jump_sound:
                print("JUMP SOUND TRIGGERED!")
                self.jump_sound.play()
            self.vel_y = self.jump_power
            self.on_ground = False
        
        self.jump_key_pressed = jump_key_down
        
        self.vel_y += self.gravity
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.y > SCREEN_HEIGHT:
            return "respawn"
        
        self.check_collisions(platforms)
        
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def die(self):
        """Trigger death with 1 second respawn delay"""
        self.is_dead = True
        self.respawn_timer = 60  # 60 frames = 1 second at 60 FPS
    
    def check_collisions(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0 and self.y < platform.top:
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = platform.bottom
                    self.vel_y = 0
    
    def draw(self, screen):
        pixel_size = 2
        y_offset = 4
        
        hat_pixels = [
            (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0),
            (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
        ]
        
        face_pixels = [
            (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2),
            (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
            (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4),
        ]
        
        shirt_pixels = [
            (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5),
            (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6),
            (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
            (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
        ]
        
        pants_pixels = [
            (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9),
            (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10),
            (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11),
            (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12),
        ]
        
        shoe_pixels = [
            (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13),
            (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14),
            (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15),
        ]
        
        eye_pixels = [
            (5, 3), (9, 3)
        ]
        
        mustache_pixels = [
            (5, 4), (6, 4), (8, 4), (9, 4)
        ]
        
        button_pixels = [
            (7, 6), (7, 7)
        ]
        
        for px, py in hat_pixels:
            pygame.draw.rect(screen, RED, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in face_pixels:
            pygame.draw.rect(screen, PINK, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in shirt_pixels:
            pygame.draw.rect(screen, RED, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in pants_pixels:
            pygame.draw.rect(screen, BLUE, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in shoe_pixels:
            pygame.draw.rect(screen, BLACK, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in eye_pixels:
            pygame.draw.rect(screen, BLACK, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in mustache_pixels:
            pygame.draw.rect(screen, BLACK, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in button_pixels:
            pygame.draw.rect(screen, YELLOW, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))

class Platform:
    def __init__(self, x, y, width, height, number=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.number = number
    
    def draw(self, screen):
        # Main platform color
        pygame.draw.rect(screen, BROWN, self.rect)
        
        # Add brick pattern
        brick_width = 20
        brick_height = 10
        
        for y in range(self.rect.top, self.rect.bottom, brick_height):
            for x in range(self.rect.left, self.rect.right, brick_width):
                # Alternate brick pattern
                offset = (brick_width // 2) if ((y - self.rect.top) // brick_height) % 2 else 0
                brick_x = x + offset
                
                if brick_x + brick_width <= self.rect.right:
                    # Draw brick outline
                    pygame.draw.rect(screen, (101, 67, 33), (brick_x, y, brick_width, brick_height), 1)
                    
                    # Add highlight on top and left
                    pygame.draw.line(screen, (160, 120, 80), (brick_x, y), (brick_x + brick_width - 1, y))
                    pygame.draw.line(screen, (160, 120, 80), (brick_x, y), (brick_x, y + brick_height - 1))
        
        # Platform border
        pygame.draw.rect(screen, (101, 67, 33), self.rect, 2)
        
        # Draw platform number
        if self.number > 0:  # Don't show number 0 (ground platform)
            font = pygame.font.Font(None, 24)
            number_text = font.render(str(self.number), True, WHITE)
            text_x = self.rect.centerx - number_text.get_width() // 2
            text_y = self.rect.centery - number_text.get_height() // 2
            screen.blit(number_text, (text_x, text_y))

class Enemy:
    def __init__(self, x, y, platform_left, platform_right):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = 2
        self.direction = 1
        self.platform_left = platform_left
        self.platform_right = platform_right
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.is_defeated = False
        self.defeat_timer = 0
    
    def update(self):
        if self.is_defeated:
            self.defeat_timer -= 1
            return self.defeat_timer <= 0  # Return True when should be removed
        
        self.x += self.speed * self.direction
        
        if self.x <= self.platform_left or self.x + self.width >= self.platform_right:
            self.direction *= -1
        
        self.rect.x = self.x
        self.rect.y = self.y
        return False
    
    def defeat(self):
        """Mark enemy as defeated"""
        self.is_defeated = True
        self.defeat_timer = 60  # 1 second before disappearing
    
    def draw(self, screen):
        pixel_size = 2
        y_offset = 1.5
        
        if self.is_defeated:
            # Draw collapsed/flattened turtle sprite
            collapsed_shell_pixels = [
                (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
                (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9),
            ]
            
            collapsed_pattern_pixels = [
                (3, 8), (5, 8), (7, 8), (9, 8),
                (4, 9), (6, 9), (8, 9),
            ]
            
            for px, py in collapsed_shell_pixels:
                pygame.draw.rect(screen, DARK_GREEN, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
            
            for px, py in collapsed_pattern_pixels:
                pygame.draw.rect(screen, YELLOW, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
            
            return
        
        # Normal turtle sprite
        shell_pixels = [
            (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
            (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
            (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4),
            (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5),
            (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6),
            (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        ]
        
        head_pixels = [
            (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
            (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
        ]
        
        legs_pixels = [
            (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
            (3, 9), (4, 9), (8, 9), (9, 9),
            (3, 10), (4, 10), (8, 10), (9, 10),
        ]
        
        eye_pixels = [
            (4, 1), (8, 1)
        ]
        
        shell_pattern_pixels = [
            (4, 3), (6, 3), (8, 3),
            (3, 4), (5, 4), (7, 4), (9, 4),
            (4, 5), (6, 5), (8, 5),
        ]
        
        for px, py in shell_pixels:
            pygame.draw.rect(screen, DARK_GREEN, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in head_pixels:
            pygame.draw.rect(screen, GREEN, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in legs_pixels:
            pygame.draw.rect(screen, GREEN, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in eye_pixels:
            pygame.draw.rect(screen, BLACK, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))
        
        for px, py in shell_pattern_pixels:
            pygame.draw.rect(screen, YELLOW, (self.x + px * pixel_size, self.y + (py + y_offset) * pixel_size, pixel_size, pixel_size))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
    
    def draw(self, screen):
        if not self.collected:
            center_x = self.x + self.width//2
            center_y = self.y + self.height//2
            radius = self.width//2
            
            # Main coin body (golden gradient effect)
            pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), radius)
            
            # Inner bright highlight
            pygame.draw.circle(screen, (255, 255, 150), (center_x - 2, center_y - 2), radius//2)
            
            # Outer dark edge
            pygame.draw.circle(screen, (180, 140, 0), (center_x, center_y), radius, 2)
            
            # Add a sparkle effect
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 3, center_y - 3), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 2, center_y + 4), 1)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Initialize background music and sound effects
    try:
        print("Initializing audio...")
        jump_sound = create_jump_sound()
        coin_sound = create_coin_sound()
        death_sound = create_death_sound()
        enemy_defeat_sound = create_enemy_defeat_sound()
        print("Sound effects created")
        
        background_music = create_background_music()
        background_music.play(-1)  # Loop indefinitely
        print("Background music started")
    except Exception as e:
        print(f"Could not initialize audio: {e}")
        background_music = None
        jump_sound = None
        coin_sound = None
        death_sound = None
        enemy_defeat_sound = None
    
    player = Player(100, 100, jump_sound)
    score = 0
    
    platforms = [
        Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, 0),  # Ground - no number
        Platform(150, 520, 100, 20, 1),
        Platform(280, 480, 160, 20, 2),
        Platform(50, 440, 80, 20, 3),
        Platform(480, 420, 100, 20, 4),
        Platform(630, 380, 160, 20, 5),
        Platform(200, 360, 80, 20, 6),
        Platform(430, 340, 60, 20, 7),
        Platform(100, 280, 100, 20, 8),
        Platform(550, 280, 80, 20, 9),
        Platform(330, 220, 160, 20, 10),
        Platform(700, 200, 80, 20, 11),
        Platform(150, 190, 100, 20, 12),
        Platform(450, 140, 80, 20, 13),
        Platform(600, 100, 100, 20, 14),
        Platform(250, 80, 60, 20, 15),
    ]
    
    enemies = [
        Enemy(25, 535, 0, 800),
        Enemy(320, 455, 280, 440),
        Enemy(670, 355, 630, 790),
        Enemy(370, 195, 330, 490),
    ]
    
    coins = [
        Coin(175, 490),
        Coin(225, 490),
        Coin(330, 450),
        Coin(380, 450),
        Coin(70, 410),
        Coin(100, 410),
        Coin(510, 390),
        Coin(560, 390),
        Coin(680, 350),
        Coin(730, 350),
        Coin(230, 330),
        Coin(450, 310),  # Adjusted for platform 7 (moved from x=400 to x=430)
        Coin(130, 250),
        Coin(180, 250),
        Coin(580, 250),  # Adjusted for platform 9 (moved from y=260 to y=280)
        Coin(380, 190),
        Coin(430, 190),
        Coin(730, 170),
        Coin(180, 160),  # Adjusted for platform 12 (moved from y=160 to y=190)
        Coin(480, 110),
        Coin(630, 70),
        Coin(680, 70),
        Coin(280, 50),
        Coin(50, 530),
        Coin(750, 530),
    ]
    
    game_won = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_won:
                    player.x = 100
                    player.y = 100
                    player.vel_y = 0
                    score = 0
                    for coin in coins:
                        coin.collected = False
                    game_won = False
        
        if not game_won:
            result = player.update([platform.rect for platform in platforms])
            if result == "respawn":
                player.die()
                score = max(0, score - 5)
            
            enemies_to_remove = []
            for i, enemy in enumerate(enemies):
                should_remove = enemy.update()
                if should_remove:
                    enemies_to_remove.append(i)
                    continue
                
                if not player.is_dead and not enemy.is_defeated and player.rect.colliderect(enemy.rect):
                    # Check if player is jumping on enemy (from above)
                    if player.vel_y > 0 and player.y < enemy.y:
                        # Player stomps on enemy
                        if enemy_defeat_sound:
                            print("ENEMY DEFEAT SOUND TRIGGERED!")
                            enemy_defeat_sound.play()
                        enemy.defeat()
                        player.vel_y = -8  # Small bounce
                        score += 50  # Bonus points for defeating enemy
                    else:
                        # Enemy defeats player
                        if death_sound:
                            print("DEATH SOUND TRIGGERED!")
                            death_sound.play()
                        player.die()
                        score = max(0, score - 10)
            
            # Remove defeated enemies that have timed out
            for i in reversed(enemies_to_remove):
                enemies.pop(i)
            
            for coin in coins:
                if not player.is_dead and not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collected = True
                    score += 10
                    if coin_sound:
                        print("COIN SOUND TRIGGERED!")
                        coin_sound.play()
            
            if all(coin.collected for coin in coins):
                game_won = True
        
        # Sky gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)  # Light blue to white
            g = int(206 + (255 - 206) * color_ratio)
            b = int(235 + (255 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        for platform in platforms:
            platform.draw(screen)
        
        for coin in coins:
            coin.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        if not game_won and not player.is_dead:
            player.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        coins_collected = sum(1 for coin in coins if coin.collected)
        coins_text = font.render(f"Coins: {coins_collected}/{len(coins)}", True, BLACK)
        screen.blit(coins_text, (10, 50))
        
        if game_won:
            win_text = font.render("CONGRATULATIONS! YOU WON!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(win_text, win_rect)
            
            restart_text = font.render("Press R to restart", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
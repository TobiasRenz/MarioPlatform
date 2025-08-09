import pygame
import math
pygame.init()

# Fenster (volle Bildschirmgröße in Pydroid)
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Pygame Touch-Steuerung mit Multitouch & Wand")
clock = pygame.time.Clock()

# Spieler
player = pygame.Rect(100, 100, 50, 50)
SPEED = 5

# Buttons
btn_left  = pygame.Rect(50,  1500, 100, 100)
btn_right = pygame.Rect(250, 1500, 100, 100)
btn_up    = pygame.Rect(700, 1500, 100, 100)
btn_down  = pygame.Rect(870, 1500, 100, 100)

# Wand
wall = pygame.Rect(500, 500, 200, 200) # For collision
visual_wall = wall.copy() # For drawing


# Coins
coins = [
    pygame.Rect(800, 200, 25, 25),
    pygame.Rect(300, 800, 25, 25),
    pygame.Rect(100, 400, 25, 25),
    pygame.Rect(900, 600, 25, 25),
    pygame.Rect(500, 300, 25, 25)
]


# Aktive Finger (Richtung, ID)
active_fingers = set()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.FINGERDOWN:
            x = event.x * screen.get_width()
            y = event.y * screen.get_height()

            if btn_left.collidepoint(x, y):
                active_fingers.add(("left", event.finger_id))
            if btn_right.collidepoint(x, y):
                active_fingers.add(("right", event.finger_id))
            if btn_up.collidepoint(x, y):
                active_fingers.add(("up", event.finger_id))
            if btn_down.collidepoint(x, y):
                active_fingers.add(("down", event.finger_id))

        elif event.type == pygame.FINGERUP:
            active_fingers = {f for f in active_fingers if f[1] != event.finger_id}

    # Bewegung
    old_pos = player.copy()

    directions = set(d for d, _ in active_fingers)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        directions.add("left")
    if keys[pygame.K_RIGHT]:
        directions.add("right")
    if keys[pygame.K_UP]:
        directions.add("up")
    if keys[pygame.K_DOWN]:
        directions.add("down")

    if "left" in directions:
        player.x -= SPEED
    if "right" in directions:
        player.x += SPEED
    if "up" in directions:
        player.y -= SPEED
    if "down" in directions:
        player.y += SPEED

    # Kollision
    if player.colliderect(wall):
        player = old_pos  # Zurücksetzen bei Kollision

    # Coin collision
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)

    # Magical effect when all coins are collected
    if not coins:
        # Pulsing effect (shrinking inward)
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 15
        visual_wall.width = wall.width - pulse
        visual_wall.height = wall.height - pulse
        visual_wall.center = wall.center
        wall_color = (138, 43, 226) # Dark purple
    else:
        visual_wall = wall.copy()
        wall_color = (150, 150, 150) # Grey

    # Zeichnen
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)   # Spieler
    pygame.draw.rect(screen, wall_color, visual_wall) # Wand
    
    for coin in coins:
        pygame.draw.rect(screen, (255, 255, 0), coin) # Coin

    pygame.draw.rect(screen, (100, 100, 100), btn_left)
    pygame.draw.rect(screen, (100, 100, 100), btn_right)
    pygame.draw.rect(screen, (100, 100, 100), btn_up)
    pygame.draw.rect(screen, (100, 100, 100), btn_down)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
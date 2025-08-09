import pygame
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
wall = pygame.Rect(500, 500, 200, 200)

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

    # Bewegung + Kollision
    old_pos = player.copy()

    for direction, _fid in active_fingers:
        if direction == "left":
            player.x -= SPEED
        elif direction == "right":
            player.x += SPEED
        elif direction == "up":
            player.y -= SPEED
        elif direction == "down":
            player.y += SPEED

    if player.colliderect(wall):
        player = old_pos  # Zurücksetzen bei Kollision

    # Zeichnen
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)   # Spieler
    pygame.draw.rect(screen, (150, 150, 150), wall) # Wand

    pygame.draw.rect(screen, (100, 100, 100), btn_left)
    pygame.draw.rect(screen, (100, 100, 100), btn_right)
    pygame.draw.rect(screen, (100, 100, 100), btn_up)
    pygame.draw.rect(screen, (100, 100, 100), btn_down)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

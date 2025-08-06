import pygame
import sys
import random

pygame.init()

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

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
        
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
    
    def check_collisions(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = platform.bottom
                    self.vel_y = 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)

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
    
    def update(self):
        self.x += self.speed * self.direction
        
        if self.x <= self.platform_left or self.x + self.width >= self.platform_right:
            self.direction *= -1
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

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
            pygame.draw.circle(screen, YELLOW, (self.x + self.width//2, self.y + self.height//2), self.width//2)
            pygame.draw.circle(screen, BLACK, (self.x + self.width//2, self.y + self.height//2), self.width//2, 2)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    player = Player(100, 100)
    score = 0
    
    platforms = [
        Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        Platform(200, 500, 200, 20),
        Platform(500, 400, 200, 20),
        Platform(100, 350, 150, 20),
        Platform(600, 250, 150, 20),
        Platform(300, 180, 100, 20),
    ]
    
    enemies = [
        Enemy(220, 475, 200, 400),
        Enemy(520, 375, 500, 700),
        Enemy(120, 325, 100, 250),
        Enemy(620, 225, 600, 750),
    ]
    
    coins = [
        Coin(250, 470),
        Coin(350, 470),
        Coin(550, 370),
        Coin(650, 370),
        Coin(150, 320),
        Coin(200, 320),
        Coin(650, 220),
        Coin(700, 220),
        Coin(350, 150),
        Coin(50, 540),
        Coin(750, 540),
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        result = player.update([platform.rect for platform in platforms])
        if result == "respawn":
            player.x = 100
            player.y = 100
            player.vel_y = 0
            score = max(0, score - 5)
        
        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                player.x = 100
                player.y = 100
                player.vel_y = 0
                score = max(0, score - 10)
        
        for coin in coins:
            if not coin.collected and player.rect.colliderect(coin.rect):
                coin.collected = True
                score += 10
        
        screen.fill(WHITE)
        
        for platform in platforms:
            platform.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        for coin in coins:
            coin.draw(screen)
        
        player.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
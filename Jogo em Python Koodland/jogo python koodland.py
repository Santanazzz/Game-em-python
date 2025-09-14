import random
import math
from pygame import Rect  # permitido pela exceção

# =============================
# CONFIGURAÇÕES DO JOGO
# =============================
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Tutor Test"
FPS = 60

# =============================
# ESTADOS GLOBAIS
# =============================
game_state = "menu"   # "menu", "playing", "gameover"
music_on = True
score = 0
lives = 3

# =============================
# ASSETS (NOMES DOS ARQUIVOS)
# =============================
hero_idle = ["hero_idle1", "hero_idle2"]
hero_run = ["hero_run1", "hero_run2", "hero_run3", "hero_run4"]
enemy_walk = ["enemy1", "enemy2"]

background_music = "bg_music"
jump_sound = "jump"
hit_sound = "hit"
click_sound = "click"

# =============================
# CLASSES
# =============================

class Hero:
    """Classe principal do jogador (herói)."""
    def __init__(self, pos):
        self.actor = Actor(hero_idle[0], pos)
        self.vy = 0
        self.on_ground = False
        self.frame = 0
        self.anim_timer = 0
        self.direction = 1  # 1 = direita, -1 = esquerda

    def update(self):
        keys = keyboard
        # gravidade
        self.vy += 0.5
        self.actor.y += self.vy

        # chão
        if self.actor.y >= HEIGHT - 70:
            self.actor.y = HEIGHT - 70
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # movimento horizontal
        if keys.left:
            self.actor.x -= 4
            self.direction = -1
            self.animate(hero_run)
        elif keys.right:
            self.actor.x += 4
            self.direction = 1
            self.animate(hero_run)
        else:
            self.animate(hero_idle)

        # pulo
        if keys.space and self.on_ground:
            self.vy = -11
            sounds[jump_sound].play()

    def animate(self, frames):
        """Gerencia troca de frames do sprite."""
        self.anim_timer += 1
        if self.anim_timer % 8 == 0:
            self.frame = (self.frame + 1) % len(frames)
            self.actor.image = frames[self.frame]
        self.actor.flip_x = self.direction == -1

    def draw(self):
        self.actor.draw()


class Enemy:
    """Classe dos inimigos que patrulham em limites definidos."""
    def __init__(self, pos, bounds):
        self.actor = Actor(enemy_walk[0], pos)
        self.bounds = bounds
        self.direction = 1
        self.frame = 0
        self.anim_timer = 0

    def update(self):
        self.actor.x += self.direction * 2
        # inverter direção ao bater nos limites
        if self.actor.x < self.bounds[0] or self.actor.x > self.bounds[1]:
            self.direction *= -1
        self.animate(enemy_walk)

    def animate(self, frames):
        self.anim_timer += 1
        if self.anim_timer % 15 == 0:
            self.frame = (self.frame + 1) % len(frames)
            self.actor.image = frames[self.frame]
        self.actor.flip_x = self.direction == -1

    def draw(self):
        self.actor.draw()


# =============================
# OBJETOS INICIAIS
# =============================
hero = Hero((100, HEIGHT - 70))
enemies = [
    Enemy((400, HEIGHT - 70), (350, 500)),
    Enemy((650, HEIGHT - 70), (600, 750))
]

# =============================
# MENU PRINCIPAL
# =============================
menu_buttons = [
    {"label": "Start Game", "rect": Rect(300, 200, 200, 50)},
    {"label": "Toggle Music", "rect": Rect(300, 300, 200, 50)},
    {"label": "Quit", "rect": Rect(300, 400, 200, 50)},
]

def draw_menu():
    screen.fill((30, 30, 30))
    screen.draw.text("Platformer Tutor Test",
                     center=(WIDTH // 2, 100),
                     fontsize=60, color="white")
    for b in menu_buttons:
        screen.draw.filled_rect(b["rect"], (80, 80, 80))
        screen.draw.text(b["label"],
                         center=b["rect"].center,
                         fontsize=40, color="white")

# =============================
# HUD (VIDAS E PONTOS)
# =============================
def draw_hud():
    screen.draw.text(f"Lives: {lives}", (20, 20), fontsize=40, color="white")
    screen.draw.text(f"Score: {score}", (20, 60), fontsize=40, color="yellow")

# =============================
# GAME OVER
# =============================
def draw_gameover():
    screen.fill("darkred")
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50),
                     fontsize=80, color="white")
    screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 20),
                     fontsize=50, color="yellow")
    screen.draw.text("Click to return to Menu",
                     center=(WIDTH // 2, HEIGHT // 2 + 100),
                     fontsize=40, color="white")

# =============================
# LOOP PRINCIPAL
# =============================
def update():
    global game_state, score, lives
    if game_state == "playing":
        hero.update()
        for e in enemies:
            e.update()
            if hero.actor.colliderect(e.actor):
                sounds[hit_sound].play()
                lives -= 1
                hero.actor.pos = (100, HEIGHT - 70)  # reset posição
                if lives <= 0:
                    game_state = "gameover"
        # aumenta pontuação ao longo do tempo
        score += 1

def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        screen.blit("background", (0, 0))
        hero.draw()
        for e in enemies:
            e.draw()
        draw_hud()
    elif game_state == "gameover":
        draw_gameover()

# =============================
# INPUTS (MOUSE)
# =============================
def on_mouse_down(pos):
    global game_state, music_on, score, lives
    if game_state == "menu":
        for b in menu_buttons:
            if b["rect"].collidepoint(pos):
                sounds[click_sound].play()
                if b["label"] == "Start Game":
                    score = 0
                    lives = 3
                    game_state = "playing"
                elif b["label"] == "Toggle Music":
                    music_on = not music_on
                    if music_on:
                        music.play(background_music)
                    else:
                        music.stop()
                elif b["label"] == "Quit":
                    exit()
    elif game_state == "gameover":
        game_state = "menu"

# =============================
# START MUSIC
# =============================
if music_on:
    music.play(background_music)

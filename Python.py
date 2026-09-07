import sys
import math
import random
import pygame

# Initialize Pygame
pygame.init()

# Display Setup
info = pygame.display.Info()
WIDTH = info.current_w if info.current_w > 0 else 360
HEIGHT = info.current_h if info.current_h > 0 else 640
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Color Palette
BG = (8, 4, 22)
PINK = (255, 105, 180)
LIGHT_PINK = (255, 192, 203)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

# Safe Default Fonts (Avoids system font errors)
FONT_TEXT = pygame.font.Font(None, int(HEIGHT * 0.035))
FONT_BTN = pygame.font.Font(None, int(HEIGHT * 0.032))

# Word Wrapping Helper
def get_wrapped_lines(text, font, max_w):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_w:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

# Background Stars
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(1, 2.5), random.uniform(-0.4, -0.1)] for _ in range(50)]

# Heart Math Function
def get_heart_pt(t, scale):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
    return (int(WIDTH / 2 + x * scale), int(HEIGHT * 0.28 + y * scale))

# Messages Sequence
messages = [
    "Hey Aditi...",
    "I had a crush on you since the opening of coaching.",
    "I really like you and I'm deeply interested in you.",
    "I promise to always be loyal and stand by your side.",
    "I promise to care for you with all my heart, throughout life.",
    "Aditi, will you give me the chance to prove this promise?"
]

idx = 0
typed = ""
char_i = 0
last_time = pygame.time.get_ticks()
accepted = False
heart_phase = 0.0

btn_w, btn_h = int(WIDTH * 0.45), int(HEIGHT * 0.06)
yes_btn = pygame.Rect(int(WIDTH * 0.5 - btn_w // 2), int(HEIGHT * 0.82), btn_w, btn_h)

# Main Loop
running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if char_i >= len(messages[idx]) and idx < len(messages) - 1:
                idx += 1
                typed = ""
                char_i = 0
            elif idx == len(messages) - 1 and char_i >= len(messages[idx]) and yes_btn.collidepoint(event.pos):
                accepted = True

    # Typewriter Effect Logic
    target = messages[idx]
    if char_i < len(target) and now - last_time > 40:
        typed += target[char_i]
        char_i += 1
        last_time = now

    screen.fill(BG)

    # Render Floating Stars
    for s in stars:
        s[1] += s[3]
        if s[1] < 0:
            s[1] = HEIGHT
        pygame.draw.circle(screen, LIGHT_PINK, (int(s[0]), int(s[1])), int(s[2]))

    # Render Heart
    heart_phase += 0.04
    scale = (HEIGHT * 0.0075) + math.sin(heart_phase) * 0.4
    pts = [get_heart_pt(t / 100, scale) for t in range(0, 628)]
    if len(pts) > 1:
        pygame.draw.polygon(screen, PINK if not accepted else GOLD, pts, width=2)

    # Render Text Content
    if not accepted:
        color = GOLD if "Aditi" in typed else LIGHT_PINK
        lines = get_wrapped_lines(typed, FONT_TEXT, int(WIDTH * 0.85))
        
        start_y = HEIGHT * 0.52
        for line in lines:
            surf = FONT_TEXT.render(line, True, color)
            rect = surf.get_rect(center=(WIDTH // 2, start_y))
            screen.blit(surf, rect)
            start_y += surf.get_height() + 8

        if char_i >= len(target) and idx < len(messages) - 1:
            sub = FONT_BTN.render("(Tap screen to continue)", True, WHITE)
            screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT * 0.76)))

        if idx == len(messages) - 1 and char_i >= len(target):
            pygame.draw.rect(screen, PINK, yes_btn, border_radius=12)
            btn_txt = FONT_BTN.render("I Accept ❤️", True, BG)
            screen.blit(btn_txt, btn_txt.get_rect(center=yes_btn.center))
    else:
        lines = get_wrapped_lines("I Will Always Keep My Promise, Aditi ❤️", FONT_TEXT, int(WIDTH * 0.85))
        start_y = HEIGHT * 0.55
        for line in lines:
            surf = FONT_TEXT.render(line, True, GOLD)
            rect = surf.get_rect(center=(WIDTH // 2, start_y))
            screen.blit(surf, rect)
            start_y += surf.get_height() + 8

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

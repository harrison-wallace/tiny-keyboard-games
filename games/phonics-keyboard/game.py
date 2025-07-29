import pygame  # type: ignore
import sys
import os

pygame.init()
pygame.mixer.init()  # Explicitly initialize mixer
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

custom_font_path = 'SchoolYard-Regular.otf'
title_font = pygame.font.Font(custom_font_path, 150)  # Larger font for titles
game_font = pygame.font.Font(custom_font_path, 1200)  # Font for in-game letters
menu_font = pygame.font.Font(custom_font_path, 100)   # Font for menus and end screen
countdown_font = pygame.font.Font(custom_font_path, 300)  # Font for countdown

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Letters to display

correct_sound = pygame.mixer.Sound('correct.wav')

# Load alphabet sounds (assuming files like 'alphasounds-a.mp3' to 'alphasounds-z.mp3' exist)
alphabet_sounds = {letter.lower(): pygame.mixer.Sound(f"phonic-sounds/alphasounds-{letter.lower()}.mp3") for letter in letters}

def animate_bounce(upper, lower):
    for i in range(10):  # 10 frames of bounce animation
        offset = (i % 5) * 20 if i < 5 else (10 - i % 5) * 20  # Up and down bounce
        combined_text = f"{upper} {lower}"
        text = game_font.render(combined_text, True, (0, 0, 255))
        screen.fill((255, 255, 255))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - offset))
        pygame.display.flip()
        pygame.time.wait(50)  # 50ms per frame

def countdown():
    for text in ["3", "2", "1", "Go!"]:
        screen.fill((255, 255, 255))
        countdown_text = countdown_font.render(text, True, (0, 0, 0))
        screen.blit(countdown_text, (width // 2 - countdown_text.get_width() // 2, height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # 1 second per number

def draw_gradient_background(start_color, end_color):
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

while True:  # Main loop for retries
    # Start menu with gradient background
    draw_gradient_background((135, 206, 235), (255, 255, 255))  # Light blue to white
    title_text = title_font.render("Alphabet Game", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 150))
    screen.blit(title_text, title_rect)
    
    # Draw "Ready" button
    ready_text = menu_font.render("Ready", True, (0, 0, 0))
    ready_rect = ready_text.get_rect(center=(width // 2, height // 2))
    ready_button_rect = pygame.Rect(ready_rect.left - 20, ready_rect.top - 20, ready_rect.width + 40, ready_rect.height + 40)
    pygame.draw.rect(screen, (0, 255, 0), ready_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), ready_button_rect, 2)
    screen.blit(ready_text, ready_rect)

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Allow window close via X button
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()  # Allow exit with ESC key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button_rect.collidepoint(event.pos):
                    waiting = False
    
    # Game play
    current_index = 0
    times = []
    
    while current_index < len(letters):
        current_letter_upper = letters[current_index]
        current_letter_lower = current_letter_upper.lower()
        current_sound = alphabet_sounds[current_letter_lower]
        sound_length_ms = current_sound.get_length() * 1000
        
        start_time = pygame.time.get_ticks()
        
        screen.fill((255, 255, 255))
        combined_text = f"{current_letter_upper} {current_letter_lower}"
        text = game_font.render(combined_text, True, (0, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()
        
        current_sound.play()
        last_play_time = start_time
        
        correct_pressed = False
        while not correct_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Allow window close via X button
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()  # Allow exit with ESC key
                    pressed_key = pygame.key.name(event.key).upper()
                    if pressed_key in letters:  # Only accept A-Z keys
                        if pressed_key == current_letter_upper:
                            correct_pressed = True
                            break
            # Check if it's time to replay the sound (after duration + 1 second)
            current_time = pygame.time.get_ticks()
            if current_time - last_play_time > sound_length_ms + 1000:
                current_sound.play()
                last_play_time = current_time
        
        end_time = pygame.time.get_ticks()
        time_taken = (end_time - start_time) / 1000
        times.append(time_taken)
        
        screen.fill((0, 255, 0))
        combined_text = f"{current_letter_upper} {current_letter_lower}"
        text = game_font.render(combined_text, True, (0, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()
        correct_sound.play()
        pygame.time.wait(3000)
        
        animate_bounce(current_letter_upper, current_letter_lower)
        
        if current_index < len(letters) - 1:
            countdown()
        
        current_index += 1
    
    # End screen with total time and average
    total_time = sum(times)
    avg_time = total_time / len(times) if times else 0
    
    draw_gradient_background((135, 206, 235), (255, 255, 255))
    total_text = menu_font.render(f"Total Time: {total_time:.2f}s", True, (0, 0, 0))
    avg_text = menu_font.render(f"Average Time: {avg_time:.2f}s", True, (0, 0, 0))
    screen.blit(total_text, (width // 2 - total_text.get_width() // 2, height // 2 - 150))
    screen.blit(avg_text, (width // 2 - avg_text.get_width() // 2, height // 2 - 50))
    
    # Draw "Retry" button
    retry_text = menu_font.render("Retry", True, (0, 0, 0))
    retry_rect = retry_text.get_rect(center=(width // 2 - 150, height // 2 + 100))
    retry_button_rect = pygame.Rect(retry_rect.left - 20, retry_rect.top - 20, retry_rect.width + 40, retry_rect.height + 40)
    pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), retry_button_rect, 2)
    screen.blit(retry_text, retry_rect)
    
    # Draw "Exit" button
    exit_text = menu_font.render("Exit", True, (0, 0, 0))
    exit_rect = exit_text.get_rect(center=(width // 2 + 150, height // 2 + 100))
    exit_button_rect = pygame.Rect(exit_rect.left - 20, exit_rect.top - 20, exit_rect.width + 40, exit_rect.height + 40)
    pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
    screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()
    
    ended = True
    while ended:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Allow window close via X button
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()  # Allow exit with ESC key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    ended = False
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
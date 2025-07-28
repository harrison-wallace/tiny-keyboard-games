import pygame  # type: ignore
import sys
import os

# Remove or comment out the dummy driver now that real audio is set up
# os.environ['SDL_AUDIODRIVER'] = 'dummy'  # No longer needed

pygame.init()
pygame.mixer.init()  # Explicitly initialize mixer
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
font = pygame.font.Font(None, 1200)  # Large font for letter display
small_font = pygame.sysfont.SysFont('NotoColorEmoji', 300)  # Emoji font
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Letters to display
current_index = 0
score = 0

# Load success sound (ensure 'correct.wav' exists)
correct_sound = pygame.mixer.Sound('correct.wav')  # Get a free WAV file if needed

# Load alphabet sounds (assuming files like 'alphasounds-a.mp3' to 'alphasounds-z.mp3' exist in the directory)
alphabet_sounds = {letter.lower(): pygame.mixer.Sound(f"alphasounds-{letter.lower()}.mp3") for letter in letters}

def animate_bounce(letter):
    for i in range(10):  # 10 frames of bounce animation
        offset = (i % 5) * 20 if i < 5 else (10 - i % 5) * 20  # Up and down bounce
        text = font.render(letter, True, (0, 0, 255))  # Blue for fun
        screen.fill((255, 255, 255))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - offset))
        pygame.display.flip()
        pygame.time.wait(50)  # 50ms per frame

while current_index < len(letters):
    current_letter = letters[current_index]
    current_sound = alphabet_sounds[current_letter.lower()]
    sound_length_ms = current_sound.get_length() * 1000  # Sound duration in milliseconds
    
    # Draw the letter
    screen.fill((255, 255, 255))  # White background
    text = font.render(current_letter, True, (0, 0, 0))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.flip()
    
    # Play the sound initially
    current_sound.play()
    last_play_time = pygame.time.get_ticks()
    
    # Inner loop for repeating sound with 1-second gap until correct key press
    while True:
        correct_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                pressed_key = pygame.key.name(event.key).upper()
                if pressed_key == current_letter:
                    score += 1
                    correct_pressed = True
                    break  # Exit the for loop early
        
        if correct_pressed:
            # Step 1: Turn background green with letter visible, play success sound, stay for 3 seconds
            screen.fill((0, 255, 0))  # Green background
            text = font.render(current_letter, True, (0, 0, 0))  # Render letter again on green
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.flip()
            correct_sound.play()  # Play success sound
            pygame.time.wait(3000)  # Pause for 3 seconds
            
            # Step 2: Bounce animation (back to white background)
            animate_bounce(current_letter)
            
            # Step 3: Show star emojis temporarily
            screen.fill((255, 255, 255))
            stars = small_font.render("⭐⭐⭐", True, (255, 215, 0))  # Gold stars
            screen.blit(stars, (width // 2 - stars.get_width() // 2, height // 2 - stars.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(1000)  # Show stars for 1 second
            
            current_index += 1
            break  # Break the while True loop to move to next letter
        
        # Check if it's time to replay the sound (after duration + 1 second)
        current_time = pygame.time.get_ticks()
        if current_time - last_play_time > sound_length_ms + 1000:
            current_sound.play()
            last_play_time = current_time

# Game over screen
screen.fill((255, 255, 255))
text = font.render(f"Score: {score}/{len(letters)}", True, (0, 0, 0))
screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)  # Show for 3 seconds
pygame.quit()
import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Define dark mode colors
DARK_BACKGROUND = (30, 30, 30)  # Dark gray/black background
WHITE = (255, 255, 255)  # White for text
YELLOW = (255, 223, 0)   # Yellow for highlighted text
RED = (255, 69, 58)      # Bright red for winner message
GREEN = (0, 255, 0)      # Green for player names or success
BLUE = (100, 149, 237)   # Blue for player turn indicator

# Set up display
WIDTH, HEIGHT = 1200, 600  # Increased width for better name display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Timer Game (Dark Mode)")

# Set fonts
font = pygame.font.SysFont("Arial", 46)
timer_font = pygame.font.SysFont("Arial", 72)
small_font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 50)

# Load topics from file
def load_topics(file_path):
    with open(file_path, 'r') as file:
        topics = file.readlines()
    return [topic.strip() for topic in topics]

# Load topics from the uploaded file
topics_list = load_topics("Topics.txt")

# Initialize scores
player1_score = 0
player2_score = 0

# Function to reset game variables
def reset_game(keep_names=False, keep_time=False):
    global player1_name, player2_name, game_time, timer_value, is_increasing, game_started, input_stage, game_ended, current_turn, selected_topic

    if not keep_names:
        player1_name = ""
        player2_name = ""

    if not keep_time:
        game_time = 0

    timer_value = 0
    is_increasing = True
    game_started = False
    input_stage = 0 if not keep_names else 3  # Skip name input if keeping names
    game_ended = False
    current_turn = "Player 1"  # Player 1 starts the game
    selected_topic = random.choice(topics_list)  # Randomly select a topic for the game
    topics_list.remove(selected_topic)

# Initialize game variables
reset_game()

# Game loop
running = True
while running:
    screen.fill(DARK_BACKGROUND)  # Dark background suited for dark mode

    if not game_started and not game_ended:
        # Collect input stage-wise
        if input_stage == 0:
            prompt = "Enter Player 1 Name: " + player1_name
        elif input_stage == 1:
            prompt = "Enter Player 2 Name: " + player2_name
        elif input_stage == 2:
            prompt = "Enter Game Time (seconds): " + (str(game_time) if game_time > 0 else "")

        # Render input prompt with bright white text
        prompt_surface = font.render(prompt, True, WHITE)
        screen.blit(prompt_surface, (50, 150))

        # Start the game when all input is done
        if input_stage == 3:
            prompt = "Topic is: " + selected_topic + "              Press ENTER to start the game"
            prompt_surface = font.render(prompt, True, YELLOW)  # Highlighted yellow text for starting
            screen.blit(prompt_surface, (50, 150))

    elif game_started and not game_ended:
        # Render the game timer with bright white text
        minutes, seconds = divmod(timer_value, 60)
        timer_display = f"{minutes:02}:{seconds:02}"
        timer_surface = timer_font.render(timer_display, True, WHITE)
        screen.blit(timer_surface, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        # Display Player 1 and Player 2 names and their winning conditions
        player1_surface = big_font.render(f"{player1_name} (Wins at 0.0 seconds)", True, GREEN)
        player2_surface = big_font.render(f"{player2_name} (Wins at {game_time:.1f} seconds)", True, GREEN)

        screen.blit(player1_surface, (50, 50))  # Display Player 1 on the left
        screen.blit(player2_surface, (WIDTH - player2_surface.get_width() - 50, 50))  # Display Player 2 on the right

        # Display whose turn it is
        if current_turn == "Player 1":
            turn_message = f"{player1_name} is guessing"
        else:
            turn_message = f"{player2_name} is guessing"
        
        turn_surface = font.render(turn_message, True, BLUE)
        screen.blit(turn_surface, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

        # Display the selected topic
        topic_surface = font.render(f"Topic: {selected_topic}", True, YELLOW)
        screen.blit(topic_surface, (WIDTH // 2 - 200, HEIGHT // 4))

    elif game_ended:
        # Display winner and update scores
        end_surface = font.render(end_text, True, RED)  # Red text for the winner
        screen.blit(end_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 50))


        # Display the current scores
        score_surface = font.render(f"Scores: {player1_name}: {player1_score} | {player2_name}: {player2_score}", True, WHITE)
        screen.blit(score_surface, (WIDTH // 2 - 200, HEIGHT // 2))

        # Display restart options
        restart_prompt = font.render("Press ENTER to restart the game", True, WHITE)
        change_names_prompt = font.render("Press S to change Settings", True, WHITE)

        screen.blit(restart_prompt, (WIDTH // 2 - 200, HEIGHT // 2 + 50))
        screen.blit(change_names_prompt, (WIDTH // 2 - 200, HEIGHT // 2 + 100))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Input handling before the game starts
        if not game_started and not game_ended:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_stage == 3:
                    # Start the game
                    timer_value = game_time // 2  # Start at midpoint
                    is_increasing = True
                    game_started = True
                    last_time = time.time()

                elif event.key == pygame.K_BACKSPACE:
                    if input_stage == 0:
                        player1_name = player1_name[:-1]
                    elif input_stage == 1:
                        player2_name = player2_name[:-1]
                    elif input_stage == 2:
                        game_time = int(str(game_time)[:-1]) if game_time > 0 else 0

                else:
                    if input_stage == 0 and event.unicode.isalpha():
                        player1_name += event.unicode
                    elif input_stage == 1 and event.unicode.isalpha():
                        player2_name += event.unicode
                    elif input_stage == 2 and event.unicode.isdigit():
                        game_time = game_time * 10 + int(event.unicode)

                if event.key == pygame.K_RETURN:
                    if input_stage == 0 and player1_name:
                        input_stage = 1
                    elif input_stage == 1 and player2_name:
                        input_stage = 2
                    elif input_stage == 2 and game_time > 0:
                        input_stage = 3

        # Handle spacebar for toggling timer direction and changing turn during the game
        if game_started and not game_ended and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_increasing = not is_increasing

                # Switch turns
                if current_turn == "Player 1":
                    current_turn = "Player 2"
                else:
                    current_turn = "Player 1"

        # Handle restarting the game after it ends
        if game_ended and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game(keep_names=True, keep_time=True)  # Restart game with same names and time
            elif event.key == pygame.K_s:
                reset_game(keep_names=False, keep_time=False)  # Change settings

    # Game logic to increase or decrease timer
    if game_started and not game_ended:
        current_time = time.time()
        if current_time - last_time >= 1:  # Update every second
            if is_increasing:
                timer_value += 1
            else:
                timer_value -= 1
            last_time = current_time

        # Check if game has ended
        if timer_value <= 0:
            end_text = f"{player1_name} wins!"
            game_started = False
            game_ended = True
            player1_score += 1

        elif timer_value >= game_time:
            end_text = f"{player2_name} wins!"
            game_started = False
            game_ended = True
            player2_score += 1

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()

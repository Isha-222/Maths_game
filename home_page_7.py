import pygame
import sys
import main_2
from main_2 import Game, screen_height, screen_width
from random import randint

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
main_2.screen = screen

# Screen Caption.
pygame.display.set_caption("Maths Invaders")

# Frame rate
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font("Pixeled.ttf", 48)
font_medium = pygame.font.Font("Pixeled.ttf", 20)
font_small = pygame.font.Font("Pixeled.ttf", 14)


class Button:
    # Clickable button on screen
    def __init__(self, x, y, width, height, text, colour, hover_colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour

    def draw(self, surface):
        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_colour = self.hover_colour
        else:
            current_colour = self.colour

        # Draw  button rectangle
        pygame.draw.rect(surface, current_colour, self.rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=10)

        # Draw button text centred inside the button
        text_surface = font_medium.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Return True if the button was clicked this event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class HomeScreen:
    def __init__(self):
        self.start_button = Button(300, 350, 200, 55, "START", (50, 141, 168), (35, 100, 120))
        self.quit_button = Button(300, 420, 200, 55, "QUIT", (156,11,11), (110, 0, 0))

    def draw(self, surface):
        # Fill background 
        surface.fill((0, 0, 0))

        # Game title
        title_surface = font_large.render("MATHS INVADERS", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 180))
        surface.blit(title_surface, title_rect)

        # Subtitle
        sub_surface = font_small.render("Answer maths questions to defeat the alien attack!", True, (80, 80, 80))
        sub_rect = sub_surface.get_rect(center=(screen_width // 2, 250))
        surface.blit(sub_surface, sub_rect)

        # Buttons
        self.start_button.draw(surface)
        self.quit_button.draw(surface)

    def handle_event(self, event):
        if self.start_button.is_clicked(event):
            return "topic"
        if self.quit_button.is_clicked(event):
            return "quit"
        return None


class TopicScreen:
    def __init__(self):
        self.topics = [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
            "Fractions",
            "Algebra",
        ]        

        self.selected_topic = None

        # Build topic buttons in a grid
        self.topic_buttons = []
        button_width = 240
        button_height = 50
        start_x = 165
        start_y = 170
        gap_x = 250
        gap_y = 70

        for i in range(len(self.topics)):

            col = i % 2
            row = i // 2

            x = start_x + col * gap_x
            y = start_y + row * gap_y

            topic = self.topics[i]

            btn = Button(x,y,button_width,button_height,topic,(145, 181, 178),(56, 110, 106))

            self.topic_buttons.append(btn)

        # Back button 
        self.back_button = Button(40, 530, 130, 44, "Back", (145, 181, 178), (56, 110, 106))

        # Confirm button
        self.confirm_button = Button(590, 530, 170, 44, "Confirm", (121, 173, 83), (42, 94, 28))

    def draw(self, surface):
        # Fill the background
        surface.fill((0, 0, 0))

        # Draw the heading
        heading = font_large.render("Select a Topic", True, (255, 255, 255))
        heading_rect = heading.get_rect(center=(screen_width // 2, 90))
        surface.blit(heading, heading_rect)

        # Draw each topic button
        for i in range(len(self.topic_buttons)):

            btn = self.topic_buttons[i]

            if self.topics[i] == self.selected_topic:
                pygame.draw.rect(surface, (220, 120, 30), btn.rect, 4, border_radius=10)

            btn.draw(surface)

        # Show which topic is currently selected
        if self.selected_topic:
            label = font_small.render("Selected: " + self.selected_topic, True, (255, 255, 255))
        else:
            label = font_small.render("Pick a topic to continue", True, (120, 120, 120))
        label_rect = label.get_rect(center=(screen_width // 2, 450))
        surface.blit(label, label_rect)

        # Draw back button
        self.back_button.draw(surface)

        # Only draw confirm in active colour if a topic is selected
        if self.selected_topic:
            self.confirm_button.colour = (121, 173, 83)
            self.confirm_button.hover_colour = (42, 94, 28)
        else:
            self.confirm_button.colour = (180, 180, 180)
            self.confirm_button.hover_colour = (180, 180, 180)
        self.confirm_button.draw(surface)

    def handle_event(self, event):
        # Check if a topic button was clicked
        for i in range(len(self.topic_buttons)):

            if self.topic_buttons[i].is_clicked(event):
                self.selected_topic = self.topics[i]

        # Back button returns to home
        if self.back_button.is_clicked(event):
            self.selected_topic = None
            return "home"

        # Confirm only works if a topic has been selected
        if self.selected_topic and self.confirm_button.is_clicked(event):
            return "difficulty"

        return None

class DifficultyScreen:
    def __init__(self):
        self.difficulties = ["Easy","Medium","Hard"]
        self.selected_difficulty = None

        # Difficulty buttons.
        self.difficulty_buttons =[]
        button_width = 210
        button_height = 50
        gap_x = 230
        start_y = 280

        for i in range(len(self.difficulties)):
            x = (screen_width // 2 - gap_x) + i * gap_x
            btn = Button(x - button_width // 2, start_y, button_width, button_height, self.difficulties[i], (121, 173, 83), (42, 94, 28))
            self.difficulty_buttons.append(btn)

        # Back and confirm buttons
        self.back_button = Button(40, 530, 130, 44, "Back", (145, 181, 178), (56, 110, 106))
        self.confirm_button = Button(590, 530, 170, 44, "Confirm", (121, 173, 83), (42, 94, 28))

    def draw(self,surface):
        # Fill background
        surface.fill((0,0,0))

        # Heading.
        heading = font_large.render("Select Difficulty", True, (255,255,255))  
        heading_rect = heading.get_rect(center=(screen_width//2,100))
        surface.blit(heading,heading_rect)

        # Draw each difficulty button.
        for i in range(len(self.difficulty_buttons)):
            btn = self.difficulty_buttons[i]
            if self.difficulties[i] == self.selected_difficulty:
                pygame.draw.rect(surface,(220,120,30),btn.rect,4,border_radius=10)
            btn.draw(surface)
                

        if self.selected_difficulty:
            label = font_small.render("Selected:" + self.selected_difficulty, True, (255,255,255))
        else:
            label = font_small.render("pick a difficulty to continue", True,(120,120,120))
        label_rect = label.get_rect(center=(screen_width//2,460))
        surface.blit(label,label_rect)

        # Back button.
        self.back_button.draw(surface)

    # Confirm button greyed out until selection is made.
        if self.selected_difficulty:
            self.confirm_button.colour = (121, 173, 83)
            self.confirm_button.hover_colour = (42, 94, 28)
        else:
            self.confirm_button.colour = (180, 180, 180)
            self.confirm_button.hover_colour = (180, 180, 180)
        self.confirm_button.draw(surface)

    def handle_event(self,event):
        # Check if a topic button was clicked.
        for i in range(len(self.difficulty_buttons)):
            if self.difficulty_buttons[i].is_clicked(event):
                self.selected_difficulty = self.difficulties[i]

        # Back button returns to topic selection.
        if self.back_button.is_clicked(event):
            self.selected_difficulty = None
            return "topic"

        if self.selected_difficulty and self.confirm_button.is_clicked(event):
            return "game"

        return None

# Set up the screens.
home_screen = HomeScreen()
topic_screen = TopicScreen()
difficulty_screen = DifficultyScreen()

# Track which screen is currently showing.
current_screen = "home"
space_game = None

# Main game loop.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "game" and space_game is not None:
            if event.type ==pygame.USEREVENT + 1:
                space_game.alien_shoot()
            if space_game.question_mode:
                space_game.handle_question(event)

        # Pass the event to active screen.
        if current_screen == "home":
            result = home_screen.handle_event(event)
            if result == "quit":
                running = False
            elif result:
                current_screen = result

        elif current_screen == "topic":
            result = topic_screen.handle_event(event)
            if result:
                current_screen = result

        elif current_screen =="difficulty":
            result = difficulty_screen.handle_event(event)
            if result:
                current_screen = result 


    # Draw current screen.
    if current_screen == "home":
        home_screen.draw(screen)
    elif current_screen == "topic":
        topic_screen.draw(screen)
    elif current_screen =="difficulty":
        difficulty_screen.draw(screen)
    elif current_screen == "game":
        if space_game is None:
            space_game = Game(topic_screen.selected_topic, difficulty_screen.selected_difficulty)
            ALIENLASER =pygame.USEREVENT + 1
            pygame.time.set_timer(ALIENLASER,800)
        screen.fill((30, 30, 30))
        space_game.run()
    # Update the display.
    pygame.display.update()
    clock.tick(60)

# Pygame exit.
pygame.quit()
sys.exit()
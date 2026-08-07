import pygame
import sys
import os
import main_2
from main_2 import Game, screen_height, screen_width
from random import randint

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
main_2.screen = screen

# Screen Caption.
pygame.display.set_caption("Maths Invaders")

# Frame rate.
clock = pygame.time.Clock()

# Fonts.
font_large = pygame.font.Font("Pixeled.ttf", 48)
font_medium = pygame.font.Font("Pixeled.ttf", 20)
font_small = pygame.font.Font("Pixeled.ttf", 14)

# Buttons.
class Button:
    def __init__(self, x, y, width, height, text, colour, hover_colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour

    def draw(self, surface):
        # Check if the mouse is hovering over the button.
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_colour = self.hover_colour
        else:
            current_colour = self.colour

        # Draw button rectangle.
        pygame.draw.rect(surface, current_colour, self.rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=10)

        # Draw button text centred inside the button.
        text_surface = font_medium.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Return True if the button was clicked this event.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Home menu screen.
class HomeScreen:
    def __init__(self):
        self.start_button = Button(290, 275, 240, 55, "START", (50, 141, 168), (35, 100, 120))
        self.leaderboard_button =  Button(290, 340, 240, 55, "LEADERBOARD", (200, 160, 40), (150, 115, 20))
        self.how_to_play_button = Button(290, 405, 240, 55, "HOW TO PLAY", (130, 120, 180), (90, 80, 140))
        self.quit_button = Button(290, 470, 240, 55, "QUIT", (156,11,11), (110, 0, 0))
        

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
        self.leaderboard_button.draw(surface)
        self.how_to_play_button.draw(surface)
        self.quit_button.draw(surface)

    def handle_event(self, event):
        if self.start_button.is_clicked(event):
            return "topic"
        if self.leaderboard_button.is_clicked(event):
            return "leaderboard"
        if self.how_to_play_button.is_clicked(event):
            return "how_to_play"
        if self.quit_button.is_clicked(event):
            return "quit"
        return None

class HowToPlayScreen:
    def __init__(self):
        # List of instructions in lines.
        self.lines = ["Pick a topic and difficulty, then enter your name.",
                    "Aliens will shoot lasers towards you.",
                    " use LEFT and RIGHT arrows to move, SPACE to shoot.",
                    "You start with 5 ammo. Each shot uses 1 ammo.",
                    "When ammo hits 0, you must answer 5 maths questions.",
                    "Correct answers give +2 ammo each and +100 points.",
                    "If you still have 0 ammo after the 5 questions, you lose a life.",
                    "You have 3 lives. Lose them all and the game ends.",
                    "Clear all the aliens to win!"]

        self.back_button = Button(40, 530, 130, 44, "Back", (145, 181, 178), (56, 110, 106))

    def draw(self, surface):
        surface.fill((0, 0, 0))
        heading = font_large.render("How To Play", True, (255, 255, 255))
        surface.blit(heading, heading.get_rect(center=(screen_width // 2, 60)))

        # Draw each instruction line 
        y = 130
        for line in self.lines:
            line_surf = font_small.render(line, True, (255, 255, 255))
            surface.blit(line_surf, line_surf.get_rect(center=(screen_width // 2, y)))
            y += 34

        self.back_button.draw(surface)

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            return "home"
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
            return "name_entry"

        return None

class NameEntryScreen:
    def __init__(self):
        self.name = ""
        self.max_len = 12
        self.box_rect = pygame.Rect(screen_width // 2 - 150, 260, 300, 50)
        self.confirm_button = Button(screen_width // 2 - 110, 350, 220, 50, "Start Game", (121, 173, 83), (42, 94, 28))
        self.back_button = Button(40, 530, 130, 44, "Back", (145, 181, 178), (56, 110, 106))

    def reset(self):
        # Clear the name so the next player gets an empty input box to type in.
        self.name = ""

    def draw(self,surface):
        surface.fill((0,0,0))

        heading= font_medium.render("Enter Your Name", True, (255, 255, 255))
        surface.blit(heading, heading.get_rect(center=(screen_width // 2, 150)))

        sub =font_small.render("This is how your score will be saved", True, (255, 255, 255))
        surface.blit(sub, sub.get_rect(center=(screen_width // 2, 200)))

        # Draw the name input box.
        pygame.draw.rect(surface, (255, 255, 255), self.box_rect, border_radius=6)
        pygame.draw.rect(surface, (0, 200, 0), self.box_rect, 2, border_radius=6)
        text_surf = font_medium.render(self.name, True, (0, 0, 0))
        surface.blit(text_surf, (260, 260)) 

        # Confirm button greyed out until a name has been entered.
        if self.name.strip():
            self.confirm_button.colour = (121, 173, 83)
            self.confirm_button.hover_colour = (42, 94, 28)
        else:
            self.confirm_button.colour = (180, 180, 180)
            self.confirm_button.hover_colour = (180, 180, 180)
        self.confirm_button.draw(surface)
        self.back_button.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character typed.
                self.name = self.name[:-1]
            elif event.key == pygame.K_RETURN:
                # Submit name and start the game.
                if self.name.strip():
                    return "game"
            else:
                # Only letters are allowed in the name.
                if (event.unicode.isalpha()) and len(self.name) < self.max_len:
                    self.name += event.unicode

        # Back button returns to difficulty selection.
        if self.back_button.is_clicked(event):
            return "difficulty"
        
        # Confirm only works once a name has been typed.
        if self.name.strip() and self.confirm_button.is_clicked(event):
            return "game"

        return None
        
class LeaderBoardScreen:
        def __init__(self):
            self.topics = ["All", "Addition", "Subtraction", "Multiplication", "Division", "Fractions", "Algebra"]
            self.difficulties = ["All", "Easy", "Medium", "Hard"]
            self.selected_topic = "All"
            self.selected_difficulty = "All"
            self.topic_buttons=[]

            # Topic filter buttons built in a column.
            y = 200
            for topic in self.topics:
                btn = Button(20, y, 240, 40, topic, (145, 181, 178), (56, 110, 106))
                self.topic_buttons.append(btn)
                y += 40

            # Difficulty filter buttons built in a row.
            self.difficulty_buttons = []
            x = 110
            for difficulty in self.difficulties:
                btn = Button(x, 140, 140, 40, difficulty, (121, 173, 83), (42, 94, 28))
                self.difficulty_buttons.append(btn)
                x += 150

            self.back_button = Button(40, 530, 130, 44, "Back", (145, 181, 178), (56, 110, 106))

        # If no scores are saved yet then the file does not exist.
        def load_scores(self):
            if not os.path.exists("leaderboard.txt"):
                return []

            entries =[]
            with open("leaderboard.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 4:
                        continue
                    name, topic, difficulty, score = parts
                    entries.append({"name": name, "topic": topic, "difficulty": difficulty, "score": int(score)})
            return entries  

        # Filter the leaderboard by the topic and difficulty.         
        def get_filtered_scores(self):
            entries = self.load_scores()
            if self.selected_topic != "All":
                entries = [e for e in entries if e["topic"] == self.selected_topic]
            if self.selected_difficulty != "All":
                entries = [e for e in entries if e["difficulty"] == self.selected_difficulty]
            entries.sort(key=lambda e: e["score"], reverse=True)
            # Only top 10 entries are displayed 
            return entries[:10]
        
        def draw(self, surface):
            surface.fill((0, 0, 0))
            heading = font_large.render("Leaderboard", True, (255, 255, 255))
            sub = font_medium.render("-Top 10-", True, (255, 255, 255))
            surface.blit(heading, heading.get_rect(center=(screen_width // 2, 60)))
            surface.blit(sub, sub.get_rect(center=(screen_width // 2, 120)))

            # Highlight the currently selected topic button.
            for i in range(len(self.topic_buttons)):
                btn = self.topic_buttons[i]
                if self.topics[i] == self.selected_topic:
                    pygame.draw.rect(surface, (220, 120, 30), btn.rect, 3, border_radius=10)
                btn.draw(surface)


            # Highlight the currently selected difficulty button.
            for i in range(len(self.difficulty_buttons)):
                btn = self.difficulty_buttons[i]
                if self.difficulties[i] == self.selected_difficulty:
                    pygame.draw.rect(surface, (220, 120, 30), btn.rect, 3, border_radius=10)
                btn.draw(surface)

            # Draw the scores ranked by highest first and filtered by category.
            entries = self.get_filtered_scores()
            y = 230

            if not entries:
                empty = font_small.render("No scores yet", True, (120, 120, 120))
                surface.blit(empty, empty.get_rect(center=(screen_width // 2, y)))
            else:
                for i in range(len(entries)):
                    entry = entries[i]
                    line = str(i + 1) + ". " + entry["name"] + " - " + str(entry["score"])
                    line_surf = font_small.render(line, True, (255, 255, 255))
                    surface.blit(line_surf, (screen_width // 2 - 100, y + i * 26))

            self.back_button.draw(surface)

        # Check if a topic filter button was clicked
        def handle_event(self, event):
            for i in range(len(self.topic_buttons)):
                if self.topic_buttons[i].is_clicked(event):
                    self.selected_topic = self.topics[i]

            # Check if a difficulty filter button was clicked
            for i in range(len(self.difficulty_buttons)):
                if self.difficulty_buttons[i].is_clicked(event):
                    self.selected_difficulty = self.difficulties[i]

            # Back button returns to home.
            if self.back_button.is_clicked(event):
                return "home"

            return None
                    
# Set up the screens.
home_screen = HomeScreen()
topic_screen = TopicScreen()
difficulty_screen = DifficultyScreen()
name_entry_screen = NameEntryScreen()
leaderboard_screen = LeaderBoardScreen()
how_to_play_screen = HowToPlayScreen()

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
            if event.type ==pygame.USEREVENT + 1 and not space_game.question_mode:
                space_game.alien_shoot()
            if space_game.question_mode:
                space_game.handle_question(event)
            space_game.handle_exit_button(event)

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

        elif current_screen == "name_entry":
            result = name_entry_screen.handle_event(event)
            if result:
                current_screen = result

        elif current_screen == "leaderboard":
            result = leaderboard_screen.handle_event(event)
            if result:
                current_screen = result

        elif current_screen == "how_to_play":
            result = how_to_play_screen.handle_event(event)
            if result:
                current_screen = result

    # Draw current screen.
    if current_screen == "home":
        home_screen.draw(screen)

    elif current_screen == "topic":
        topic_screen.draw(screen)

    elif current_screen =="difficulty":
        difficulty_screen.draw(screen)

    elif current_screen == "name_entry":
        name_entry_screen.draw(screen)

    elif current_screen == "leaderboard":
        leaderboard_screen.draw(screen)

    elif current_screen == "how_to_play":
        how_to_play_screen.draw(screen)

    # Build the game object once, if it has already been built keep reusing it for every frame.
    elif current_screen == "game":
        if space_game is None:
            space_game = Game(topic_screen.selected_topic, difficulty_screen.selected_difficulty, name_entry_screen.name.strip())
            ALIENLASER =pygame.USEREVENT + 1
            pygame.time.set_timer(ALIENLASER,800)
        screen.fill((30, 30, 30))
        space_game.run()

        # Send player to leaderboard after game is finished.
        if space_game.game_over:
            pygame.display.update()
            pygame.time.wait(100)
            current_screen = "leaderboard"
            space_game = None
            name_entry_screen.reset()
            topic_screen.selected_topic = None
            difficulty_screen.selected_difficulty = None

        # If the player chose to exit send them back to the menu.
        elif space_game.exit_to_menu:
            current_screen = "home"
            space_game = None
            name_entry_screen.reset()
            topic_screen.selected_topic = None
            difficulty_screen.selected_difficulty = None

    # Update the display.
    pygame.display.update()
    clock.tick(60)

# Pygame exit.
pygame.quit()
sys.exit()
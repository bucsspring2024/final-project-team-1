import pygame
import requests
import sys
import pygame.mixer


pygame.init()
pygame.mixer.init()

WIDTH = 500
HEIGHT = 500
fps = 144
api_key = '30d4741c779ba94c470ca1f63045390a'

class Button:
    def __init__(self, screen,font, txt, pos):
        self.screen = screen
        self.font = font
        self.text = txt
        self.pos = pos
        self.button = pygame.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(self.screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(self.screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = self.font.render(self.text, True, 'black')
        self.screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))
        
class Controller():
    def __init__(self):
    
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('Weather Forecast')

        pygame.mixer.music.load("weather.mp3")
        pygame.mixer.music.play(-1)  # -1 makes the music play indefinitely

        self.main_menu = True  # Start with the main menu
        self.settings_menu = False
        self.search_menu = False
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.menu_command = 0

    def fetch_weather_data(self, city):
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")
        if weather_data.json()['cod'] == '404':
            return None
        else:
            return {
                'weather': weather_data.json()['weather'][0]['main'],
                'temp': round(weather_data.json()['main']['temp']),
                'humidity': weather_data.json()['main']['humidity'],
                'wind_speed': weather_data.json()['wind']['speed']
            }

    def display_weather_data(self, city, weather_data):
        if weather_data is None:
            return "No weather data found"
        else:
            return f"Weather in {city}:\n- {weather_data['weather']}\n- Temperature: {weather_data['temp']}°F\n- Humidity: {weather_data['humidity']}%\n- Wind Speed: {weather_data['wind_speed']} mph"
   

    def draw_menu(self):
        command = -1
        pygame.draw.rect(self.screen, 'white', [120, 120, 260, 40], 0, 5)
        pygame.draw.rect(self.screen, 'gray', [120, 120, 260, 40], 5, 5)
        txt = self.font.render('Weather Forecast!', True, 'black')
        self.screen.blit(txt, (135, 127))
        button1 = Button(self.screen, self.font, 'Search', (120, 180))
        button1.draw()
        button2 = Button(self.screen, self.font, 'Setting', (120, 240))
        button2.draw()
        if button1.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.search_menu = True
            command = 1
        if button2.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.settings_menu = True
            command = 2
        return command

    def draw_settings(self):
        command = -1
        # Draw the Settings title
        pygame.draw.rect(self.screen, 'white', [120, 120, 260, 40], 0, 5)
        pygame.draw.rect(self.screen,  'gray', [120, 120, 260, 40], 5, 5)
        txt = self.font.render('Settings', True, 'black')
        self.screen.blit(txt, (135, 127))
        
        # Create and draw buttons for Volume Pause and Unpause
        volume_pause = Button(self.screen, self.font, 'Volume Pause', (120, 180))
        volume_unpause = Button(self.screen, self.font, 'Volume Unpause', (120, 240))
        main_menu_button = Button(self.screen, self.font, 'Main Menu', (120, 300))
        
        volume_pause.draw()
        volume_unpause.draw()
        main_menu_button.draw()
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for mouse click events
        if pygame.mouse.get_pressed()[0]:  # If the mouse is clicked
            if volume_pause.button.collidepoint(mouse_pos):
                pygame.mixer.music.pause()  # Pause the music
            elif volume_unpause.button.collidepoint(mouse_pos):
                pygame.mixer.music.unpause()  # Unpause the music
            elif main_menu_button.button.collidepoint(mouse_pos):
                self.settings_menu = False
                self.main_menu = True  # Return to the main menu
    
        return command
    # Main menu button

    def draw_search(self):
        command = -1
        city = ''
        result = ''
        self.search_menu = True  # Search menu is active when this function is running
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        weather_data = self.fetch_weather_data(city)
                        result = self.display_weather_data(city, weather_data)
                    elif event.key == pygame.K_BACKSPACE:
                        city = city[:-1]
                    else:
                        city += event.unicode

            # Drawing the input and result boxes
            pygame.draw.rect(self.screen, (255, 255, 255), (50, 50, 400, 30))
            pygame.draw.rect(self.screen, (120, 120, 100), (50, 50, 400, 30), 2)
            text_surface = self.font.render("City: " + city, True, (0, 0, 0))
            self.screen.blit(text_surface, (55, 55))

            pygame.draw.rect(self.screen, (255, 255, 255), (50, 100, 400, 300))
            pygame.draw.rect(self.screen, (120, 120, 120), (50, 100, 400, 300), 2)
            result_lines = result.split('\n')
            for i, line in enumerate(result_lines):
                text_surface = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(text_surface, (55, 105 + i * 25))

            # Drawing the Search and Main Menu buttons
            pygame.draw.rect(self.screen, (200, 200, 200), (200, 420, 100, 40))
            pygame.draw.rect(self.screen, (120, 120, 100), (200, 420, 100, 40), 2)
            text_surface = self.font.render("Search", True, (0, 0, 0))
            self.screen.blit(text_surface, (210, 425))
            main_menu_button = Button(self.screen, self.font, 'Main Menu', (350, 470, 300, 50))
            main_menu_button.draw()

            pygame.display.flip()

            # Handling button clicks
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if pygame.Rect(200, 420, 100, 40).collidepoint(mouse_pos):
                    weather_data = self.fetch_weather_data(city)
                    result = self.display_weather_data(city, weather_data)
                elif main_menu_button.button.collidepoint(mouse_pos):
                    self.search_menu = False  # Deactivate search menu
                    self.main_menu = True  # Activate main menu
                    break

        return command

    def draw_search_menu(self):
        self.search_menu = True
        while self.search_menu:
            self.screen.fill('white')
            self.timer.tick(fps)
            command = self.draw_search()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.search_menu = False
                if command == 7:
                    self.search_menu = False
                return

    def draw_game(self):
        menu_btn = Button(self.screen, self.font, 'Main Menu', (230, 450))
        menu_btn.draw()
        menu = menu_btn.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        return menu

    def mainloop(self):
        
        run = True
        while run:
            self.screen.fill('white')
            self.timer.tick(fps)
            
            if self.main_menu:
                self.menu_command = self.draw_menu()
                if self.menu_command == 1:  # Assuming 1 is for search
                    self.search_menu = True
                    self.main_menu = False
                elif self.menu_command == 2:  # Assuming 2 is for settings
                    self.settings_menu = True
                    self.main_menu = False
            elif self.search_menu:
                self.draw_search_menu()
            elif self.settings_menu:
                self.draw_settings()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.flip()

        pygame.quit()


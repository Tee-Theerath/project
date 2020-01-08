#gain access to pygame library
import pygame

#game screen name, size
SCREEN_TITLE = 'Crossy RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#color according RGB color
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

clock = pygame.time.Clock()

#import font
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:
    #Typical rate of 60, equivalent to FPS
    TICK_RATE = 60
    is_game_over = False

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #create game screen with specific size
        self.game_screen = pygame.display.set_mode((width, height))

        #set game window's color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        #load and set background image for screen
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player = playable('player.png', 375, 700, 50 ,50)

        enemy = nonplayable('enemy.png', 20, 400, 50, 50)
        enemy.SPEED *= level_speed

        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        while not is_game_over: #main event in-game

            #quit type event to exit the game, most ofter mouse,button-related event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: #when press up key
                        direction = 1
                    elif event.key == pygame.K_DOWN: #when press down key
                        direction = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

                print(event)

            #Redraw background
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))

            #draw treasure
            treasure.draw(self.game_screen)

            #update player position
            player.move(direction, self.height)
            #draw player at new position
            player.draw(self.game_screen)

            enemy.move(self.width) #auto moving
            enemy.draw(self.game_screen)

            #end game if have collision
            if player.detect_collision(enemy) == True:
                is_game_over = True
                did_win = False
                text = font.render('You lose! :(', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player.detect_collision(treasure) == True:
                is_game_over = True
                did_win = True
                text = font.render('You win! :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update()  #update game graphics
            clock.tick(self.TICK_RATE)    #tick clock to update everything

        #if you win restart gameloop
        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return

#generic game object class to be subclassed by other objects in game
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        #import image
        object_image = pygame.image.load(image_path)
        #transform image
        self.image = pygame.transform.scale(object_image, (50, 50))

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    #draw object by blitting it onto the background(game screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class playable(GameObject):

    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #move function will move character up
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        #make sure the character never goes past the bottom of the screen
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    def detect_collision(self, other_body): #detect collision between 2 OBJ
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True

class nonplayable(GameObject):

    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #move function will move character left/right
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED) #positive (go right)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED) #negative (go left)
        self.x_pos += self.SPEED

pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

#quit pygame and the program
pygame.quit()
quit()

#import player
#player_image = pygame.image.load('player.png')
#transform image
#player_image = pygame.transform.scale(player_image, (50, 50))
#rect(screen, color, [posx, posy, width, height])
#pygame.draw.rect(game_screen, BLACK_COLOR, [400, 400, 100, 100])
#circle(screen, color, (posx, posy), radius)
#pygame.draw.circle(game_screen, BLACK_COLOR, (400, 300), 50)
#game_screen.blit(player_image, (375, 375))

import pygame
pygame.init()
import chesss
import checkers
from chesss import black_colour, white_colour, minutes, ScreenWidth

colour_scheme = 'black'

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screensize = pygame.display.get_window_size()
print(screensize)

screen_width = screensize[0]
screen_height = screensize[1]
colour = (999999999)
new_colour = (255,100,100)
size = 30
white = (255,255,255)
rectangles = []
rectangles_colour = []
rectangle_colour_time = []
temp_colour_time  = []
x = ScreenWidth/2 - 100
rectangle_width = 220
rectangle_height = 60


background_image = pygame.image.load(r"assets\chessBackground.jpg")
background_image = pygame.transform.scale(background_image, (screen_width,screen_height))

def hover_mouse(rectangle, x, y):
    scale = 16
    if rectangle.rectangle.collidepoint(mouse_pos):
        rectangle.colour = new_colour
        rectangle.width = rectangle_width + scale
        rectangle.height = rectangle_height + scale
        rectangle.x = x - scale/2
        rectangle.y = y - scale/2
    else:
        rectangle.colour = colour
        rectangle.width = rectangle_width
        rectangle.height = rectangle_height
        rectangle.x = x
        rectangle.y = y #makes the rectangle over which the mouse is hovering change colour and expand

def finding_x(screenwidth, rectanglewidth, i):
    centre = screenwidth / i
    half_rectangle = rectanglewidth/2
    x = centre - half_rectangle
    return x

def writingText(text, x, y, width, height, colour, size): #function for writing text
    textFont = pygame.font.Font('freesansbold.ttf', size)
    pygame.draw.rect(screen, colour, (x,y, width, height))
    textDisplay = textFont.render(str(text), True, 0)
    textRect = textDisplay.get_rect()
    textRect.center = ((x + width/2), (y + height/2))
    screen.blit(textDisplay, textRect)

class Rectangle:

    def __init__(self,x,y,width,height,text,size):
        self.x = x
        self.y= y
        self.colour = colour
        self.size = size
        self.text = text
        self.width = width
        self.height = height

        self.rectangle = pygame.Rect(x,y,width,height)

    def dislayingBoxes(self):
        writingText(self.text,self.x,self.y,self.width,self.height,self.colour,self.size)

rectangle_play = Rectangle(finding_x(screen_width,rectangle_width, 2),200,rectangle_width, rectangle_height,'Play chess',size)
rect_shad = pygame.Rect(finding_x(screen_width,rectangle_width, 2)-5,200-5,rectangle_width+10, rectangle_height+10)
rectangle_play2 = Rectangle(finding_x(screen_width,rectangle_width, 2),320,rectangle_width, rectangle_height,'Play checkers',size)
rectangle_settings = Rectangle(finding_x(screen_width,rectangle_width, 2),440,rectangle_width, rectangle_height,'Settings',size)
rectangle_exit = Rectangle(finding_x(screen_width,rectangle_width, 2),560,rectangle_width, rectangle_height,'Exit',size)
rectangle_back = 0
temp_back = Rectangle(0,0,60,50,'',size)

temp_colour_time.append(Rectangle(finding_x(screen_width,rectangle_width,2),650,rectangle_width,50,('time: '+str(chesss.minutes)),size))
temp_colour_time.append(Rectangle(finding_x(screen_width,rectangle_width,2),690,rectangle_width,50,('colours :'+str(colour_scheme)),size))

x_temp = rectangle_play.x
y_temp = rectangle_play.y
x2_temp = rectangle_play2.x
y2_temp = rectangle_play2.y
x3_temp = rectangle_settings.x
y3_temp = rectangle_settings.y

while True:
    screen.fill(0)
    screen.blit(background_image, (0, 0))

    for i in range(0,len(rectangles)):
        rectangles[i].dislayingBoxes() #these are only drawn once play game is  pressed
    if rectangle_play != 0: #because once its pressed it disapppears which would give a syntax error so needs to be checked
        pygame.draw.rect(screen, (128,128,128), rect_shad)
        rectangle_play.dislayingBoxes()
    if rectangle_play2 != 0:
        rectangle_play2.dislayingBoxes()
    if rectangle_settings != 0:
        rectangle_settings.dislayingBoxes()
    for i in range(0,len(rectangles_colour)):
        rectangles_colour[i].dislayingBoxes()
    if rectangle_back != 0:
        rectangle_back.dislayingBoxes()
        pygame.draw.polygon(screen, 0, [(10,25),(30,15),(30,35)],3)
        pygame.draw.line(screen, 0, (30,25),(50,25),3)
    for i in range(len(rectangle_colour_time)):
        rectangle_colour_time[i].dislayingBoxes()
        rectangle_colour_time[0] = Rectangle(finding_x(screen_width,200,2),650,220,50,('time: '+str(chesss.minutes)),size)
        rectangle_colour_time[1] = Rectangle(finding_x(screen_width,200,2),690,220,50,('colours: '+str(colour_scheme)),size)
    if rectangle_exit != 0:
        rectangle_exit.dislayingBoxes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYUP:
            if event.key == 27:
                exit()

        if event.type == pygame.MOUSEBUTTONUP: #gets the coordinaets of where the mouse has been pressed
            mouse_pos = pygame.mouse.get_pos()

            if rectangle_settings != 0: #has to check first because once this square is pressed it goes to 0
                if rectangle_settings.rectangle.collidepoint(mouse_pos): #is the rectangle has been pressed the screen changes so the player can choose how long they want the game to be
                    temp_play = rectangle_play
                    temp_exit = rectangle_exit
                    temp_play2 = rectangle_play2
                    rectangle_play2 = 0
                    rectangle_exit = 0
                    rectangle_play = 0
                    temp_settings = rectangle_settings
                    rectangle_settings = 0
                    rectangles.append(Rectangle(finding_x(screen_width,800, 2),0,800,50,'Choose how much time you want',40))
                    rectangles.append(Rectangle(finding_x(screen_width,800, 2),50,800,50,'and the colour scheme',40))
                    for i in range(2,11,2):
                        rectangles.append(Rectangle((finding_x(screen_width,rectangle_width, 2) - rectangle_width),(i*50+80),200,50,(str(i) + ' minutes'),size))


                    rectangles_colour.append(Rectangle((finding_x(screen_width,rectangle_width, 2) + rectangle_width),180,200,50,'black',size))
                    rectangles_colour.append(Rectangle((finding_x(screen_width,rectangle_width, 2) + rectangle_width),280,200,50,'blue',size))
                    rectangles_colour.append(Rectangle((finding_x(screen_width,rectangle_width, 2) + rectangle_width),380,200,50,'green',size))
                    rectangles_colour.append(Rectangle((finding_x(screen_width,rectangle_width, 2) + rectangle_width),480,200,50,'red',size))
                    rectangles_colour.append(Rectangle((finding_x(screen_width,rectangle_width, 2) + rectangle_width),580,200,50,'brown',size))
                    rectangle_back = temp_back
                    rectangle_back.colour = colour

                    rectangle_colour_time.append(temp_colour_time[0])
                    rectangle_colour_time.append(temp_colour_time[1])

            for i in range(0,len(rectangles)): #chooses timer
                if rectangles[i].rectangle.collidepoint(mouse_pos):
                    chesss.minutes = (i-1)*2

            if len(rectangles_colour) > 0:


                if rectangles_colour[0].rectangle.collidepoint(mouse_pos):
                    colour_scheme = 'black'
                    chesss.black_colour = (60,60,60)
                    chesss.white_colour = (255,255,255)
                    chesss.borderColour = (0)

                if rectangles_colour[1].rectangle.collidepoint(mouse_pos):
                    colour_scheme = 'blue'
                    chesss.black_colour = (0,0,100)
                    chesss.white_colour = (200,200,255)
                    chesss.borderColour = (0,0,100)

                if rectangles_colour[2].rectangle.collidepoint(mouse_pos):
                    colour_scheme = 'green'
                    chesss.black_colour = (0,100,0)
                    chesss.white_colour = (200,255,200)
                    chesss.borderColour = (0,100,0)

                if rectangles_colour[3].rectangle.collidepoint(mouse_pos):
                    colour_scheme = 'red'
                    chesss.black_colour = (100,0,0)
                    chesss.white_colour = (255,200,200)
                    chesss.borderColour = (100,0,0)

                if rectangles_colour[4].rectangle.collidepoint(mouse_pos):
                    colour_scheme = 'brown'
                    chesss.black_colour = (70,30,30)
                    chesss.white_colour = (240,200,200)
                    chesss.borderColour = (70,30,30)

            if rectangle_play != 0: #because sometimes the rctangle won't exist. if this is pressed it will start the game by running main from other file
                if rectangle_play.rectangle.collidepoint(mouse_pos):
                    exit = False
                    #chesss.seconds = 2
                    #chesss.minutes = 0
                    chesss.assigns_timers()
                    screen.blit(background_image, (0, 0))

                    while chesss.playing == True:
                        chesss.main()
                    while chesss.playing == False:
                        if chesss.current_turn == 'white':
                            chesss.endScreen('Black won', chesss.black_colour, chesss.white_colour)
                        elif chesss.current_turn == 'black':
                            chesss.endScreen('White won', chesss.white_colour, chesss.black_colour)
                        if chesss.timers[0].timer_seconds <= 0:
                            chesss.endScreen('Black won', chesss.black_colour, chesss.white_colour)
                        elif chesss.timers[1].timer_seconds <= 0:
                            chesss.endScreen('White won', chesss.white_colour, chesss.black_colour)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                                exit = True
                        if exit == True:
                            break
                        pygame.display.flip()

            if rectangle_exit != 0:
                if rectangle_exit.rectangle.collidepoint(mouse_pos):
                    exit()

            if rectangle_back != 0:
                if rectangle_back.rectangle.collidepoint(mouse_pos):
                    rectangle_play = temp_play
                    rectangle_settings = temp_settings
                    rectangle_settings.colour = colour
                    rectangle_exit = temp_exit
                    rectangle_play2 = temp_play2
                    rectangles = []
                    rectangles_colour = []
                    rectangle_back = 0
                    rectangle_colour_time = []

            if rectangle_play2 != 0:
                if rectangle_play2.rectangle.collidepoint(mouse_pos):
                    while True:
                        checkers.main()


        else: #so when you hover over a text box it changes colour and some of them expand as well
                mouse_pos = pygame.mouse.get_pos()

                if rectangle_settings != 0: #has to check first because once this square is pressed it goes to 0
                    hover_mouse(rectangle_settings, x3_temp, y3_temp)

                for i in range(0,len(rectangles)): #chooses timer
                    if rectangles[i].rectangle.collidepoint(mouse_pos):
                        if i != 0 and i !=1:
                            rectangles[i].colour = new_colour
                    else:
                        rectangles[i].colour = colour

                if len(rectangles_colour) > 0:

                    for i in rectangles_colour:
                        if i.rectangle.collidepoint(mouse_pos):
                            i.colour = new_colour
                        else:
                            i.colour = colour

                if rectangle_play != 0: #because sometimes the rctangle won't exist. if this is pressed it will start the game by running main from other file
                    hover_mouse(rectangle_play, x_temp, y_temp)

                if rectangle_play2 != 0: #because sometimes the rctangle won't exist. if this is pressed it will start the game by running main from other file
                    hover_mouse(rectangle_play2, x2_temp, y2_temp)

                if rectangle_exit != 0:
                    if rectangle_exit.rectangle.collidepoint(mouse_pos):
                        rectangle_exit.colour = new_colour
                    else:
                        rectangle_exit.colour = colour

                if rectangle_back != 0:
                    if rectangle_back.rectangle.collidepoint(mouse_pos):
                        rectangle_back.colour = new_colour
                    else:
                        rectangle_back.colour = colour


    pygame.display.flip()

import pygame
import chesss
from chesss import fromEdge_x, displayingBoard, PlayWidth, SquareWidth, fromEdge_y
'''
chesss.fromEdge_x = 30
chesss.fromEdge_y = 30
fromEdge_x = 30
fromEdge_y = 30
'''
pygame.init()
screen = pygame.display.set_mode((800,800))
white_checkers = []
black_checkers = []
new_rect_colour = (0,255,0)
current_turn = 'white'
global chosen_checker
chosen_checker = 0
global chosen_rect
chosen_rect = 0
index = 0
moved = False
red_img = 0
black_img = 0

def appending_images():
    global red_img
    global black_img
    red_img = pygame.image.load(r"assets\red.webp")
    black_img = pygame.image.load(r"assets\black.webp")

    red_img = pygame.transform.scale(red_img, (SquareWidth,SquareWidth))
    black_img = pygame.transform.scale(black_img, (SquareWidth,SquareWidth))
appending_images()
def displaying_images():
    for i in white_checkers:
        screen.blit(red_img, (i.x, i.y))
    for i in black_checkers:
        screen.blit(black_img, (i.x, i.y))

def highlighing():
    for i in white_checkers:
        if i.rect_colour != (255,255,0):
            pygame.draw.rect(screen, i.rect_colour, i.rectangle)
    for i in black_checkers:
        if i.rect_colour != (255,255,0):
            pygame.draw.rect(screen, i.rect_colour, i.rectangle)#onyl draws rect for whichever isnt the normal colour

class Checker:
    def __init__(self, x, y, colour, multiplier):
        self.x = x
        self.y = y
        self.colour = colour
        self.rect_colour = (255,255,0)
        self.rectangle = pygame.Rect(x,y,SquareWidth,SquareWidth)
        self.multiplier = multiplier
        self.move = False
        self.collided = [False,False] #first is with white then with black

    def checking_move(self, move_to):
        global current_turn
        self.collision = 0
        self.removing = [False,False] #if removing[0] is true then will remove from white, if [1] then from black

        #this section checks if the piece is trying to move diagonal and sets .move to true if yes. It takes into consideration the direction by using .multiplier because for whites y can only decrease
        if move_to[1] == (self.y + self.multiplier*SquareWidth):
            if abs(move_to[0]-self.x) == SquareWidth:
                self.move = True

        elif 2*SquareWidth == abs(move_to[1]-self.y) and 2*SquareWidth == abs(move_to[0]-self.x):
            x_check = (self.x+move_to[0])/2
            y_check = (self.y+move_to[1])/2
            rectangle_to_check = pygame.Rect(x_check, y_check, SquareWidth, SquareWidth)
            self.collision = self.checks_collisions(rectangle_to_check)
            if self.colour == 'white': #if a white piece collides with a black one while moving two diagonal
                if self.collided[1] == True:
                    self.collided[1] = False
                    self.removing[1] = True
                    self.move = True
            elif self.colour == 'black':
                if self.collided[0] == True:
                    self.collided[0] = False
                    self.removing[0] = True
                    self.move = True

        if self.move: #checks if the chosen square collides with any piece
            self.checks_collisions(move_to)

        if True in self.collided:
            self.move = False

        if self.move: #this will change the coordinates and change the curent turn to the other colour. Itll also remove if necessary
            self.removing_()
            returned = self.changing_coordintes(move_to)
            current_turn = returned[1]
            return returned[0]
        else:
            self.collided = [False,False]

    def changing_coordintes(self, move_to): #changes the x and y coordinates and the colour of the rectangle back to normal
        if self.colour == 'white':
            white_checkers[index].rectangle = move_to
            white_checkers[index].x = move_to[0]
            white_checkers[index].y = move_to[1]
            current_turn = 'black'
        else:
            black_checkers[index].rectangle = move_to
            black_checkers[index].x = move_to[0]
            black_checkers[index].y = move_to[1]
            current_turn = 'white'
        self.rect_colour = (255,255,0)
        self.move = False
        return True, current_turn

    def checks_collisions(self, rectangle): #checks collision with both colours with the rectangle given as parameter
        for i in white_checkers:
            if i.rectangle.colliderect(rectangle):
                self.collided[0] = True
                return i
        for i in black_checkers:
            if i.rectangle.colliderect(rectangle):
                self.collided[1] = True
                return i

    def removing_(self): #removes the checker from its list
        if self.removing[0] == True:
            remove_index = white_checkers.index(self.collision)
            white_checkers.pop(remove_index)
        if self.removing[1] == True:
            remove_index = black_checkers.index(self.collision)
            black_checkers.pop(remove_index)


y = fromEdge_y + 5*SquareWidth
for i in range(0,3):
    x = (i%2)*SquareWidth + fromEdge_x
    x2 = abs((i%2)-1)*SquareWidth + fromEdge_x
    for j in range(0,4):
        white_checkers.append(Checker(x, y, 'white', -1))
        black_checkers.append(Checker(x2, (y-5*SquareWidth), 'black', 1))
        x += SquareWidth*2
        x2 += SquareWidth*2
    y += SquareWidth #before the game starts it appends the two lists of pieces with their coordinates

def finding_pieces(list, mouse_pos): #list is the list of pieces who's turn it is. Looks through the pieces and highlights the right one.
    global index
    global chosen_checker
    for i in list:
        if i.rectangle.collidepoint(mouse_pos):
            if len(list) < index:
                list[index].rect_colour = (255,255,0)
            i.rect_colour = new_rect_colour
            chosen_checker = i
            index = list.index(i)
            return True

def deciding_move(mouse_pos):
    global chosen_checker
    global chosen_rect
    global index
    #when the mouse is pressed and its whites turn is searches through the list of white pieces to see if the mouse collides with any of them.
    #It changes the colour of the rectangle to a different colour.
    #creates variable called
    if current_turn == 'white':
        found = finding_pieces(white_checkers, mouse_pos)
    elif current_turn == 'black':
        found = finding_pieces(black_checkers, mouse_pos)
    if found == True:
        return

    #so that it only goes to this if you already chose the checker that you want to move
    if chosen_checker != 0:
        for i in chesss.board_rects:
            if i.collidepoint(mouse_pos):
                chosen_rect = i

        if chosen_rect != 0:
            move = chosen_checker.checking_move(chosen_rect)
            if move == True:
                return True
            else:
                return False
        else: #if outside of the board is pressed the chosen checker resets
            chosen_checker = 0
            white_checkers[index].rect_colour = (255,255,0)
            black_checkers[index].rect_colour = (255,255,0)


def main():
    global chosen_rect
    global chosen_checker

    chesss.displayingBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYUP:
            if event.key == 27:
                exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            moved = deciding_move(mouse_pos)
            if moved == True:
                chosen_rect = 0
                chosen_checker = 0
            elif moved == False:
                chosen_rect = 0


    highlighing()

    displaying_images()

    pygame.display.flip()

'''
while True:
    main()
'''

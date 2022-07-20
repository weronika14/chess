import pygame
global playing
playing = True

'''
current_piece[0] stores the name eg Pawn
current_piece[1] stores the object from class Piece
current_piece[2] stores the pygame.Rect
pressed_square stores the pygame.Rect
copy started 20.07.2022
i think the only thing im missing is en passant
'''

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screensize = pygame.display.get_window_size()

white_colour = (255,255,255)
black_colour = (60,60,60)
ScreenWidth = screensize[0] #width of the actual window
ScreenHeight = screensize[1] #height of the actual window
#PlayWidth = int(screensize[0]/2 - 72) #width and height of the chessboard on the window
PlayWidth = 600
SquareWidth = int(PlayWidth/8) #to find how big the squares are
white = (255,255,255)
borderColour = (200,200,200)
#fromEdge_x = 30
#fromEdge_y = 30
fromEdge_y = int((screensize[1]-PlayWidth)/2)
fromEdge_x = int((screensize[0]-PlayWidth)/2) #the distance the chess board is from the left of the screen, just to make it look pretty and to make it easier to move it away without having to alter the code in numerous places
pieces = ('Rook', 'Knight', 'Bishop','Queen','King','Bishop','Knight','Rook','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn')
list_pieces = ['Pawn', 'King', 'Rook', 'Queen', 'Knight', 'Bishop']
global mouse_pos
mouse_pos = []
global current_piece
current_piece = 0
global pressed_square
pressed_square = 0
global index
index = 0
board_rects = [] #all the rectanges (as pygame.Rect) that make up the board will be appended on later
board_rect_colours = []
current_piece_class = 0
piecesBlack = [[0 for i in range(3)] for j in range(16)] #creates the list for black pieces but stores 0s only
piecesWhite = [[0 for i in range(3)] for j in range(16)]
current_turn = 'white'
yellow = (250,200,100)
whiteImages = []
blackImages = []
timers = []
minutes = 10
seconds = 0
piecesBlack2 = []
piecesWhite2 = []
xy_zbite_biale = [0,(ScreenHeight-200)]
xy_zbite_czarne = [(fromEdge_x+PlayWidth+40),120]
white_moved = [False,False,False] #left rook, king, right rook
black_moved = [False,False,False] #left rook, king, right rook


def check_end_game(list1,list2, colour): #this function will check if each piece can move to each square in turn, and will return true if at least one piece is available to move. parameter list1 specifies the colour of the pieces whos turn it is, so if its whites turn list1 = piecesWhite and will check for each of these in turn if there is any place at all for them to move
    global current_piece
    global pressed_square
    attacker = []
    attacker_count = 0
    if current_piece != 0:
        temp = current_piece #zapisuje zeby na koniec zmienic spowrotem bo tu tylko zmienia zeby sprawdzic
    if pressed_square != 0:
        temp2 = pressed_square
    for i in board_rects:
        pressed_square = i #zepiuje koordynary krola w pressed square zeby potem mozna bylo sprawdzic czy kazda figura moze sie tam przesunac, bo jesli tak to znaczy ze go zbije.
        for j in range(0,len(list1)): #dla kazdej figury w jednym z kolorow patrzy czy ta figura bedzie mofla zbic krola przeciwnego koloru
            current_piece = list1[j]
            if current_piece[2] != pressed_square:
                current_piece[1].link_class()
                current_piece[1].current_piece_class.moving() #specificzne dla kazdej figury, zwroci .move i .collided zeby zobaczyc czy przsuwanie na pole krola jest mozliwe jesli tak to jest szach.
                if current_piece[1].current_piece_class.move == True:
                    if colour == 'white':
                        temp_j = piecesWhite[j][2]
                        piecesWhite[j][2] = pressed_square
                    else:
                        temp_j = piecesBlack[j][2]
                        piecesBlack[j][2] = pressed_square

                    checked = checking_king(list1, list2)

                    if colour == 'white':
                        piecesWhite[j][2] = temp_j
                    else:
                        piecesBlack[j][2] = temp_j

                    current_piece = temp
                    pressed_square = temp2
                    if checked[0] == True and checked[1] == True:
                        return True
                    if checked[0] == False:
                        return True

    return False


def endScreen(text, bg_clr, txt_clr):
    x = 1536/2-200
    y = 864/2-200
    writingText(text, x, y, 400, 400, txt_clr, bg_clr, 50)
    pygame.draw.rect(screen,txt_clr,(x,y,400,400),10)


def checking_king(list1, list2): #list1 is the list which contains the king, so if its blacks turn list1 would be piecesBlack, as it would find blacks king and check if hes under attack from anything in list2, in this scenatio piecesWhite
    global current_piece
    global pressed_square
    attacker = []
    attacker_count = 0
    if current_piece != 0:
        temp = current_piece #zapisuje zeby na koniec zmienic spowrotem bo tu tylko zmienia zeby sprawdzic
    if pressed_square != 0:
        temp2 = pressed_square
    for i in range(0,len(list1)):
        if list1[i][0] == 'King': #szuke gdzie jest krol w liscie
            pressed_square = pygame.Rect(list1[i][1].x, list1[i][1].y, SquareWidth, SquareWidth) #zepiuje koordynary krola w pressed square zeby potem mozna bylo sprawdzic czy kazda figura moze sie tam przesunac, bo jesli tak to znaczy ze go zbije.
    for i in range(0,len(list2)): #dla kazdej figury w jednym z kolorow patrzy czy ta figura bedzie mofla zbic krola przeciwnego koloru
        current_piece = list2[i]
        current_piece[1].link_class()
        current_piece[1].current_piece_class.moving() #specificzne dla kazdej figury, zwroci .move i .collided zeby zobaczyc czy przsuwanie na pole krola jest mozliwe jesli tak to jest szach.
        if current_piece[1].current_piece_class.collided:
            if list1[current_piece[1].current_piece_class.j][0] == 'King':
                attacker.append(current_piece)
                attacker_count += 1 #tak jakby wiecej niz jedna figura atakowala krola.


    current_piece = temp
    pressed_square = temp2

    if attacker_count > 0: #jesli tylko jedna figura atakuje krola.
        if attacker_count == 1:
            for i in range(0,attacker_count):
                if pressed_square.colliderect(attacker[i][2]):
                    return True, True #first returns true jesli ktos zbija krola, a drugie true jest jesli ktos zbija tego co zbija krola

            return True, False
        else:
            return True, False

    else:
        return False, False


class Timer:

    def __init__(self, minutes, seconds, adder): #starts the timer
        self.adder = adder
        self.timer_seconds = seconds
        self.timer_minutes = minutes
        self.timer = str(self.timer_minutes) + ':' + str(self.timer_seconds)
        self.timer_event = pygame.USEREVENT + adder

        pygame.time.set_timer(self.timer_event, 1000)

    def decreasing_timer(self): #so that when it gets to zero seconds the number of minutes goes down
        if self.timer_seconds == -1 and self.timer_minutes != 0:
            self.timer_seconds = 59
            self.timer_minutes -= 1
        elif self.timer_minutes == 0 and self.timer_seconds <= 0:
            self.timer = '00:00'
            global playing
            playing = False
            return
        if self.timer_seconds < 10: #so that instead of for example 1:2 minutes its 1:02 because it looks nicer so it adds a 0 at the font
            string_seconds = '0' + str(self.timer_seconds)
        else:
            string_seconds = str(self.timer_seconds)
        self.timer = str(self.timer_minutes) + ':' + string_seconds


def assigns_timers(): #this function is only called at the beginning of the program. It starts the timers depending on the time chosen.
    global timers
    timers = [Timer(minutes,seconds,0),Timer(minutes,seconds,1)]
    pygame.time.set_timer(timers[1].timer_event, 0) #at the start the black timer decreases by 0
    pygame.time.set_timer(timers[0].timer_event, 1000) #at the start the white timer decreases every 1000 ms (1 s)


def appending_images():
    whiteImages.append(pygame.image.load(r"assets\whitePawn.png"))
    whiteImages.append(pygame.image.load(r"assets\whiteKing.png"))
    whiteImages.append(pygame.image.load(r"assets\whiteRook.png"))
    whiteImages.append(pygame.image.load(r"assets\whiteQueen.png"))
    whiteImages.append(pygame.image.load(r"assets\whiteHorse.png"))
    whiteImages.append(pygame.image.load(r"assets\whiteBishop.png"))
    blackImages.append(pygame.image.load(r"assets\blackPawn.png"))
    blackImages.append(pygame.image.load(r"assets\blackKing.png"))
    blackImages.append(pygame.image.load(r"assets\blackRook.png"))
    blackImages.append(pygame.image.load(r"assets\blackQueen.png"))
    blackImages.append(pygame.image.load(r"assets\blackHorse.png"))
    blackImages.append(pygame.image.load(r"assets\blackBishop.png"))

    for i in range (0,len(whiteImages)):
        whiteImages[i] = pygame.transform.scale(whiteImages[i], (SquareWidth,SquareWidth))
    for i in range (0,len(blackImages)):
        blackImages[i] = pygame.transform.scale(blackImages[i], (SquareWidth,SquareWidth))


def displaying_images():
    for i in range(0,len(piecesBlack)): #checks what square has been pressed on and highlights it
        if piecesBlack[i][1].new_colour != 'black': #just so that the squares only show up if they are pressed on
            pygame.draw.rect(screen, piecesBlack[i][1].new_colour, piecesBlack[i][2])
        for j in range(len(list_pieces)):
            if piecesBlack[i][0] == list_pieces[j]:
                screen.blit(blackImages[j], (piecesBlack[i][1].x, piecesBlack[i][1].y))

    for i in range(0,len(piecesWhite)):
        if piecesWhite[i][1].new_colour != 'white': #just so that the squares only show up if they are pressed on
            pygame.draw.rect(screen, piecesWhite[i][1].new_colour, piecesWhite[i][2])
        for j in range(len(list_pieces)):
            if piecesWhite[i][0] == list_pieces[j]:
                screen.blit(whiteImages[j], (piecesWhite[i][1].x, piecesWhite[i][1].y))

    for i in range(0,len(piecesWhite2),3):
        for j in range(len(list_pieces)):
            if piecesWhite2[i] == list_pieces[j]:
                screen.blit(whiteImages[j], (piecesWhite2[i+1].x,piecesWhite2[i+1].y))

    for i in range(0,len(piecesBlack2),3):
        for j in range(len(list_pieces)):
            if piecesBlack2[i] == list_pieces[j]:
                screen.blit(blackImages[j], (piecesBlack2[i+1].x,piecesBlack2[i+1].y))
appending_images()


def writingText(text, x, y, width, height, txt_colour, rect_colour, size): #function for writing text
    textFont = pygame.font.Font('freesansbold.ttf', size)
    pygame.draw.rect(screen, rect_colour, (x,y, width, height))
    textDisplay = textFont.render(str(text), True, txt_colour)
    textRect = textDisplay.get_rect()
    textRect.center = ((x + width/2), (y + height/2))
    screen.blit(textDisplay, textRect)


def displayingBoard():  #making the chess board
    thickness = 30
    letters = []

    if board_rects != []: #so that the list doesn't keep getting appended cause before it just kept being appneded and there were lots of square
        for i in range(0,64):
            board_rects.pop(0)
            board_rect_colours.pop(0)
    count_x = 0

    pygame.draw.rect(screen, borderColour, ((fromEdge_x-thickness),(fromEdge_y-thickness),(PlayWidth+thickness*2),(PlayWidth+thickness*2))) #border rectangle

    for i in range(fromEdge_x, (PlayWidth+fromEdge_x), SquareWidth): #drawing grid

        for j in range(fromEdge_y, (PlayWidth+fromEdge_y), SquareWidth):
            if (count_x % 2) == 0: #so that every other square is white
                board_rects.append(pygame.Rect([i,j,SquareWidth,SquareWidth]))
                board_rect_colours.append(white_colour)
                #pygame.draw.rect(screen, white, [i,j,SquareWidth,SquareWidth])
            else:
                board_rects.append(pygame.Rect([i,j,SquareWidth,SquareWidth]))
                board_rect_colours.append((black_colour))
                #pygame.draw.rect(screen, (50,40,30), [i,j,SquareWidth,SquareWidth])
            count_x+=1
        count_x +=1
    for i in range (0,8): #doing the writing on the side of the grid (letters going horizontally)
        letter = chr(65 + i) #because A is 65, so from 65 onwards
        writingText(letter, (i*SquareWidth+fromEdge_x), (fromEdge_y-thickness), SquareWidth, (thickness), white, borderColour, 30)
        writingText(letter, (i*SquareWidth+fromEdge_x), (fromEdge_y+PlayWidth), SquareWidth, (thickness), white, borderColour, 30)
        writingText((8-i), (fromEdge_x-thickness), (i*SquareWidth+fromEdge_y), (thickness), SquareWidth, white, borderColour, 30)
        writingText((8-i), (fromEdge_x+PlayWidth), (i*SquareWidth+fromEdge_y), (thickness), SquareWidth, white, borderColour, 30)

    for j in range(0,64):
        pygame.draw.rect(screen, board_rect_colours[j], board_rects[j])

    '''
    #prints the x and y coordinates of the board, used for testing
    for i in range(fromEdge_y,ScreenWidth,SquareWidth):
        writingText(i, 0, i, fromEdge_y, SquareWidth,(255,255,255),0,20)
    for i in range(fromEdge_x,ScreenWidth,SquareWidth):
        writingText(i, i, 0, SquareWidth,fromEdge_y,(255,255,255),0,20)
    '''


def checking_move(list1, list2,mouse_pos): #the colour is to check whos move it is, list1 is either piecesWhite or piecesBlack (the one who's move it currently is)
    global current_piece
    global pressed_square
    global index

    if current_piece != 0:
        if current_piece[0] == 'King':
            for rect in board_rects:
                if rect.collidepoint(mouse_pos[0],mouse_pos[1]): #checks the coordinates of the square on which the mouse is pressed
                    if rect[1] == current_piece[1].y: #makes sure the king is moving horizontally in a straight line
                        if SquareWidth*2 == abs(current_piece[1].x - rect[0]) or rect[0] == (current_piece[1].x-4*SquareWidth) or rect[0] == (current_piece[1].x+3*SquareWidth):
                            pressed_square = rect
                            current_piece[1].moving_piece()
                            return #so that it doesn't go on to choosing pressed_square


    for i in range (0,len(list1)): #looks through the list depending on whos turn it is and if the right colour is presses the current piece is set to whateber has been pressed on
        if list1[i][2].collidepoint(mouse_pos[0],mouse_pos[1]):
            current_piece = list1[i]
            if index < len(list1):
                list1[index][1].new_colour = list1[index][1].colour
            index = i
            current_piece[1].highlight()
            return #so that it doesn't go on to choosing pressed_square

    if current_piece != 0: #will only go to this if a piece they want to move is already chosen, otherwise can't choose what square to move it to cause there't nothing to move
            for rect in board_rects:
                if rect.collidepoint(mouse_pos[0],mouse_pos[1]): #checks the coordinates of the square on which the mouse is pressed
                    pressed_square = rect


            if pressed_square != 0: #if a square to move the piece to is chosen (so isnt 0), the function to check if the piece can be moved is called
                current_piece[1].moving_piece()
            else:
                if index < len(list1):
                    list1[index][1].new_colour = list1[index][1].colour
                current_piece = 0


class Piece:

    def __init__(self, piece, colour): #all the pieces in the game are placed on their starting positions depending on their colour and type
        self.piece = piece
        self.colour = colour
        self.new_colour = colour
        self.removed = []
        if self.colour == 'black':
            if self.piece != 'Pawn':
                self.y = fromEdge_y
                self.x = fromEdge_x + i * SquareWidth
            elif self.piece == 'Pawn':
                self.y = fromEdge_y + SquareWidth
                self.x = fromEdge_x + (i-8) * SquareWidth
        elif self.colour == 'white':
            if self.piece != 'Pawn':
                self.y = fromEdge_y + SquareWidth*7
                self.x = fromEdge_x + i * SquareWidth
            elif self.piece == 'Pawn':
                self.y = fromEdge_y + SquareWidth*6
                self.x = fromEdge_x + (i-8) * SquareWidth

    def chosen_piece(self):
        type = self.linking_class()

    def link_class(self): #gets the piece on which the mouse presses and turns it into an object from another class so that it can have itss own personlaised attributes and methods
        if current_piece[0] == 'Rook':
            self.current_piece_class = Rook(self.x, self.y)
        elif current_piece[0] == 'Pawn':
            self.current_piece_class = Pawn(self.x, self.y)
        elif current_piece[0] == 'Knight':
            self.current_piece_class = Knight(self.x, self.y)
        elif current_piece[0] == 'Bishop':
            self.current_piece_class = Bishop(self.x, self.y)
        elif current_piece[0] == 'Queen':
            self.current_piece_class = Queen(self.x, self.y)
        elif current_piece[0] == 'King':
            self.current_piece_class = King(self.x, self.y)

    def highlight(self): #not done properly yet is meant to highlight the square on which the chosen piece is standing but idk how to make it disappear after another piece is pressed
        if self.colour == 'black':
            self.new_colour = (0,0,50)
        elif self.colour == 'white':
            self.new_colour = (50,0,0)
        self.link_class()

    def checking_checkmate(self):
        temp_x = self.x
        temp_y = self.y
        self.x = pressed_square[0]
        self.y = pressed_square[1]
        if current_piece[1].colour == 'white':
            temp = piecesWhite[index][2]
            piecesWhite[index][2] = pygame.Rect(self.x,self.y,SquareWidth,SquareWidth)
            result = checking_king(piecesWhite, piecesBlack)
            if result[0] == True:
                if result[1] == False:
                    self.current_piece_class.move = False
                    piecesWhite[index][2] = temp

        elif current_piece[1].colour == 'black':
            temp = piecesBlack[index][2]
            piecesBlack[index][2] = pygame.Rect(self.x,self.y,SquareWidth,SquareWidth)
            result = checking_king(piecesBlack, piecesWhite)
            if result[0] == True: #bedzie true jesli jak sie przesuniesz bialym to bezie szach na krula, wiec wtedy nie mozesz sie tam przesunac.
                if result[1] == False: #false jesli przesuwajac sie nie zbijasz figury ktora szchuje krola
                    self.current_piece_class.move = False
                    self.current_piece_class.collided = False
                    piecesBlack[index][2] = temp
        if self.current_piece_class.move == False:
            self.x = temp_x
            self.y = temp_y

    def moving_piece(self): #changes the x and y coordinates (first going to the class's method for moving to check if its allowed to do so) and updates this in the array of all the pieces
        global current_piece
        global pressed_square
        global current_turn
        global xy_zbite_biale
        global xy_zbite_czarne
        global playing, white_moved, black_moved, piecesBlack, piecesWhite
        temp2 = current_piece[2]

        castle = self.current_piece_class.moving() #each piece has its own function for checking if it can move, which is defined in the pieces class
        #this will return None for any movement apart from castling, so if the king is pressed to move to the left or right and the collision is also hecked in the king.moving() function
        if castle != None: #so if this movement is castling it goes to here because any other move would return None. If the move is catling the value returned is the new coordinate the king should move to.
            if current_piece[1].colour == 'white':
                returned = self.castling_part2(piecesWhite, castle) #if castling is true then returned will be the new modified list with king's and rooks coordinates changed, otherwise itll return None
                if returned != None:
                    piecesWhite = returned
                    current_turn = 'black'
                    pygame.time.set_timer(timers[1].timer_event, 1000) #black timer starts running
                    pygame.time.set_timer(timers[0].timer_event, 0) #white timer stop running

            elif current_piece[1].colour == 'black':
                returned = self.castling_part2(piecesBlack, castle)
                if returned != None:
                    piecesBlack = returned
                    current_turn = 'white'
                    pygame.time.set_timer(timers[0].timer_event, 1000) #black timer starts running
                    pygame.time.set_timer(timers[1].timer_event, 0) #white timer stop running

            current_piece = 0
            self.new_colour = self.colour
            pressed_square = 0
            return

        if self.current_piece_class.collided: #checks if the piece will end on the king. if yes then move will be set to false (collided is also set to false)
            if current_piece[1].colour == 'white':
                if piecesBlack[self.current_piece_class.j][0] == 'King':
                    self.current_piece_class.move = False
                    self.current_piece_class.collided = False
            if current_piece[1].colour == 'black':
                if piecesWhite[self.current_piece_class.j][0] == 'King':
                    self.current_piece_class.move = False
                    self.current_piece_class.collided = False
        if self.current_piece_class.move == True: #only if it can move, it checks if after the move this pieces king will be under attack, and then the piece wont move
            self.checking_checkmate()

        if self.current_piece_class.move == True: #if all the conditions are met and the piece is allowed to move its x and y coordinates are changed to the x and y coordinates of the square that it moves to
            if current_piece[1].colour == 'black': #changes the x and y coordinates in the list piecesBlack (at the correct index) to the new coordinates
                current_turn = 'white'
                pygame.time.set_timer(timers[0].timer_event, 1000) #white timer start running
                pygame.time.set_timer(timers[1].timer_event, 0) #black timer stop running
                if piecesBlack[index][0] == 'King': #if the piece that has just moved is king it sets it to True because then you won't be allowed to castle
                    black_moved[1] = True
                    print('black king moved')
                if self.current_piece_class.collided: #collided will only be true if the collision is with a piece of the different colour and at the chosen square, if there is a collision anywhere else move wont be true so it wont get to this part of the program.
                    piecesWhite[self.current_piece_class.j][1].x = xy_zbite_biale[0]
                    piecesWhite[self.current_piece_class.j][1].y = xy_zbite_biale[1]
                    self.appending(piecesWhite2,piecesWhite, self.current_piece_class.j)
                    self.removing_from_list(self.current_piece_class.j, piecesWhite)
                    if xy_zbite_biale[0] >= SquareWidth*3: #this sets up the pieces that have been taken off the board
                        xy_zbite_biale[0] = 0
                        xy_zbite_biale[1] -= SquareWidth
                    else:
                        xy_zbite_biale[0] += SquareWidth
                if check_end_game(piecesWhite, piecesBlack, 'white') != True:
                    playing = False


            elif current_piece[1].colour == 'white': #changes the x and y coordinates in the list piecesWhite of the correct piece
                current_turn = 'black'
                pygame.time.set_timer(timers[1].timer_event, 1000) #black timer starts running
                pygame.time.set_timer(timers[0].timer_event, 0) #white timer stop running
                if piecesWhite[index][0] == 'King':
                    print('white king moved')
                    white_moved[1] = True
                if self.current_piece_class.collided:
                    piecesBlack[self.current_piece_class.j][1].x = xy_zbite_czarne[0]
                    piecesBlack[self.current_piece_class.j][1].y = xy_zbite_czarne[1]
                    self.appending(piecesBlack2,piecesBlack, self.current_piece_class.j)
                    self.removing_from_list(self.current_piece_class.j, piecesBlack)
                    if xy_zbite_czarne[0] >= (SquareWidth*3+(fromEdge_x+PlayWidth+40)):
                        xy_zbite_czarne[0] = (fromEdge_x+PlayWidth+40)
                        xy_zbite_czarne[1] += SquareWidth
                    else:
                        xy_zbite_czarne[0] += SquareWidth
                if check_end_game(piecesBlack, piecesWhite, 'black') != True:
                    playing = False

            if temp2 == ((fromEdge_x+7*SquareWidth),(fromEdge_y+7*SquareWidth),SquareWidth,SquareWidth): #if the piece that just moved is the rook in the right corner then it moving is set to True
                white_moved[2] = True
            elif temp2 == (fromEdge_x, (fromEdge_y+7*SquareWidth),SquareWidth,SquareWidth):
                white_moved[0] = True
            elif temp2 == (fromEdge_x, fromEdge_y, SquareWidth, SquareWidth):
                black_moved[0] = True
            elif temp2 == ((fromEdge_x+7*SquareWidth), fromEdge_y, SquareWidth, SquareWidth):
                black_moved[2] = True 
            current_piece = 0
            self.new_colour = self.colour
            pressed_square = 0


        else: #goes here if the piece can't move to the chosen square. This resets the value stored at pressed_square
            pressed_square = 0

    def castling_part2(self, list1, castle): #list one is whoever move it is so if its white moving then its piecesWhite, catle is the new x coordinate of the king. This is only if the right pressed_square has been pressed and there is no collision.
        temp_x2 = list1[index][1].x
        adder = int((self.x-castle)/2) #adder will always be equal to the size of pressed square but this finds if its positive or negative
        for i in range(castle,(self.x+adder),adder): #changes the x coordinate of the pressed square temporarily to see if the king moving will be in check
            pressed_square[0] = i
            self.checking_checkmate()
        pressed_square[0] = castle #because it has been changed above
        if self.current_piece_class.move == False:
            list1[index][1].x = temp_x2
            list1[index][2].x = temp_x2
        elif self.current_piece_class.move == True: #actually moves the king and rook, this is after all the validation has been done
            self.x = castle #moves the king two places to the left or right (castle is the x coordinate where it should move)
            list1[index][2] = pygame.Rect(self.x,self.y,SquareWidth,SquareWidth)
            for i in range(len(list1)): #following section of code moves the rook. it finds where the rook is in relation to the king and moves it whichever way it needs to
                if list1[i][0] == 'Rook':
                    if list1[i][2].x == self.x + SquareWidth: #if the rook is to the right of the king
                        list1[i][2].x = self.x - SquareWidth
                        list1[i][1].x = self.x - SquareWidth
                        break
                    if list1[i][2].x == self.x - 2*SquareWidth: #if the rook is to the right of the king
                        list1[i][2].x = self.x + SquareWidth
                        list1[i][1].x = self.x + SquareWidth
                        break
            return list1

    def appending(self, list, list2, index):
        for j in list2[index]:
            list.append(j)

    def removing_from_list(self, index, list): #where index is the index of the item that is to be removed and list determined whether its white or black ths is to be removed
        self.removed = list[index] #theres something wrong here
        for j in range(0,3):
            list[index].pop(0)
            #print(self.removed)
        list.pop(index)
        print('removing',index, self.removed)


class Rook:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.collided = False
        self.move = False

    def moving(self): #checks if where its meant to be moved follows the rules, if yes returns true, otherwise false. checks collisions and range of movement
        if pressed_square[0] == self.x and pressed_square[1] != self.y:
            difference = pressed_square[1]-self.y #this is to check if it can move without colliding along the way, because as you know it can't jump over other pieces so needs to check everything along the way
            if difference < 0:
                multiplier = -1
            else:
                multiplier = 1
            for i in range((multiplier*SquareWidth), (difference), (multiplier*SquareWidth)): #checks if there are any collisions along the way or on the finaly square
                self.checks_collision(piecesWhite, self.x, (self.y+i))
                self.checks_collision(piecesBlack, self.x, (self.y+i))
            if self.collided == False:
                self.move = True


        elif pressed_square[0] != self.x and pressed_square[1] == self.y:
            difference = pressed_square[0]-self.x
            if difference < 0:
                multiplier = -1
            else:
                multiplier = 1
            for i in range((multiplier*SquareWidth), (difference), (multiplier*SquareWidth)):
                self.checks_collision(piecesWhite, (self.x+i), self.y)
                self.checks_collision(piecesBlack, (self.x+i), self.y)
            if self.collided == False:
                self.move = True


        if self.move == True:
            if current_piece[1].colour == 'white':
                self.collided = False
                self.checks_collision(piecesWhite, pressed_square[0], pressed_square[1])
                if self.collided:
                    self.move = False
                self.checks_collision(piecesBlack, pressed_square[0], pressed_square[1])
            elif current_piece[1].colour == 'black':
                self.collided = False
                self.checks_collision(piecesBlack, pressed_square[0], pressed_square[1])
                if self.collided:
                    self.move = False
                self.checks_collision(piecesWhite, pressed_square[0], pressed_square[1])

    def checks_collision(self,list,x,y):
        for i in range(0,len(list)):
            if (pygame.Rect(x,y,SquareWidth,SquareWidth)).colliderect(list[i][2]):
                self.collided = True
                self.j = i


class Pawn:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.move = False
        self.kills = False
        self.collided = False

    def moving(self): #checks if where its meant to be moved follows the rules, if yes returns true, otherwise false. checks collisions and range of movement
        self.move = False
        self.collided = False
        if current_piece[1].colour == 'black':
            self.multiplier = 1 #because when you are black you move down so y increases
        elif current_piece[1].colour == 'white':
            self.multiplier = -1 #because pawn can only move up, so y decreases


        if self.x == pressed_square[0]: #what happens when x stays the same, meaning the pawn is moving forwards in a straight line (vertically), so unless there is somethinig in the way or is trying to move too far itll return true
            if pressed_square[1] == (self.y+(self.multiplier*SquareWidth)): #checks if the chosen square is one square in front
                self.move = True
            elif pressed_square[1] == (self.y+(self.multiplier*2*SquareWidth)): #checks if the chosen square is two in front and only returns true if pawn is at its starting position
                if current_piece[1].colour == 'black':
                    if self.y == (SquareWidth+fromEdge_y): #this is the starting position of a black pawn
                        self.move = True
                elif current_piece[1].colour == 'white':
                    if self.y == (SquareWidth*6 + fromEdge_y):
                        self.move = True
            if self.move:
                self.checks_collision(piecesWhite,self.x)
                self.checks_collision(piecesBlack,self.x)
            if self.collided:
                self.move = False
                self.collided = False

        elif self.x == (pressed_square[0]+SquareWidth) or self.x == (pressed_square[0]-SquareWidth): #checks if the value of x is increased or decreased by one square
            if pressed_square[1] == (self.y+(self.multiplier*SquareWidth)): #checks if y only increases by one square and in the right direction (for a white pawn y value should decrese). self.move will only evaluate to true if these two conditions are true if self.collided is true
                if current_piece[1].colour == 'black':
                    self.checks_collision(piecesWhite, pressed_square[0])
                elif current_piece[1].colour == 'white':
                    self.checks_collision(piecesBlack, pressed_square[0]) #if pawn tried to go diagonal(and checks for collision)

                if self.collided:
                    self.move = True

    def checks_collision(self,list,x): #list is either piecesBlack or piecesWhite
        difference = abs(pressed_square[1]-self.y) #to check if it can move without colliding
        for i in range(SquareWidth, (difference+SquareWidth), SquareWidth): #checks if there will be any collision if the pawn is moved forward
            for j in range(0,len(list)):
                if (pygame.Rect(x, (self.y+(self.multiplier*i)), SquareWidth, SquareWidth)).colliderect(list[j][2]):
                    self.j = j #j is the index of the value which should be removed from the list
                    self.collided = True


class Knight:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.move = False
        self.collided = False

    def moving(self):
        for i in range(-1,2,2): #so that it works if it goes up or down because when i is negative y will  increase and when postive it will increase (knight can go any direction)
            if pressed_square[1] == (self.y+(i*2*SquareWidth)):
                if pressed_square[0] == (self.x+(i*SquareWidth)):
                    self.move = True
                if pressed_square[0] == (self.x-(i*SquareWidth)):
                    self.move = True
            if pressed_square[0] == (self.x+(i*2*SquareWidth)):
                if pressed_square[1] == (self.y+(i*SquareWidth)):
                    self.move = True
                if pressed_square[1] == (self.y-(i*SquareWidth)):
                    self.move = True

        if self.move == True:
            if current_piece[1].colour == 'white':
                self.checks_collision(piecesWhite,pressed_square[0],pressed_square[1])
                if self.collided:
                    self.move = False
                    self.collided = False
                self.checks_collision(piecesBlack,pressed_square[0],pressed_square[1])
            if current_piece[1].colour == 'black':
                self.checks_collision(piecesBlack,pressed_square[0],pressed_square[1])
                if self.collided:
                    self.move = False
                    self.collided = False
                self.checks_collision(piecesWhite,pressed_square[0],pressed_square[1])

    def checks_collision(self,list,x,y):
        for i in range(0,len(list)):
            if (pygame.Rect(x,y,SquareWidth,SquareWidth)).colliderect(list[i][2]):
                self.collided = True
                self.j = i


class Bishop:

    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.move = False
        self.collided = False

    def moving(self):
        x_difference = abs(pressed_square[0] - self.x)
        y_difference = abs(pressed_square[1] - self.y)

        if pressed_square[0] < self.x: #so that you check the squares in the right direction
            x_multiplier = -1
        else:
            x_multiplier = 1
        if pressed_square[1] < self.y:
            y_multiplier = -1
        else:
            y_multiplier = 1

        if x_difference == y_difference: #checks if it can move (if its on the right path)
            self.move = True

        y_check = self.y
        if self.move:
            for i in range((self.x+x_multiplier*SquareWidth),pressed_square[0], (x_multiplier*SquareWidth)): #check whether there is a collision along a way (not including final square)
                y_check += SquareWidth * y_multiplier
                self.checks_collision(piecesBlack,i,y_check)
                self.checks_collision(piecesWhite,i,y_check)

                if self.collided:
                    self.move = False

        if self.move == True: #if its on the right path and there is not collision along the way, this will check if there is a collision on the final squares
            if current_piece[1].colour == 'white':
                self.checks_collision(piecesBlack, pressed_square[0], pressed_square[1])
            elif current_piece[1].colour == 'black':
                self.checks_collision(piecesWhite, pressed_square[0], pressed_square[1])

    def checks_collision(self,list,x,y):
        for i in range(0,len(list)):
            if (pygame.Rect(x,y,SquareWidth,SquareWidth)).colliderect(list[i][2]):
                self.collided = True
                self.j = i


class Queen:

    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.move = False
        self.collided = False

    def moving(self):
        x_difference = abs(pressed_square[0] - self.x)
        y_difference = abs(pressed_square[1] - self.y)
        if pressed_square[0] < self.x: #so that you check the squares in the right direction
            x_multiplier = -1
        else:
            x_multiplier = 1
        if pressed_square[1] < self.y:
            y_multiplier = -1
        else:
            y_multiplier = 1

        #the following section of code check all the different ways it can move ignoring collisions.
        if x_difference == y_difference: #moves diagonal
            self.move = True

            y_check = self.y #checks collision for diogonal movement
            for i in range((self.x+x_multiplier*SquareWidth),pressed_square[0], (x_multiplier*SquareWidth)): #check whether there is a collision along a way (not including final square)
                y_check += SquareWidth * y_multiplier

                self.checks_collision(piecesBlack,i,y_check)
                self.checks_collision(piecesWhite,i,y_check)
                if self.collided:
                    self.move = False

        elif pressed_square[0] == self.x and pressed_square[1] != self.y: #moves verticlaly in a straight line
            self.move = True

            for i in range((self.y+y_multiplier*SquareWidth), pressed_square[1], (y_multiplier*SquareWidth)): #checks collision for vertical movement
                self.checks_collision(piecesBlack,self.x,i)
                self.checks_collision(piecesWhite,self.x,i)
                if self.collided:
                    self.move = False

        elif pressed_square[0] != self.x and pressed_square[1] == self.y: #moves horizontally in a straight line
            self.move = True

            for i in range((self.x+x_multiplier*SquareWidth), pressed_square[0], (x_multiplier*SquareWidth)): #checks collision for vertical movement
                self.checks_collision(piecesBlack,i,self.y)
                self.checks_collision(piecesWhite,i,self.y)
                if self.collided:
                    self.move = False


        if self.move == True: #if its on the right path and there is not collision along the way, this will check if there is a collision on the final squares
            if current_piece[1].colour == 'white':
                self.collided = False
                self.checks_collision(piecesWhite, pressed_square[0], pressed_square[1])
                if self.collided:
                    self.move = False
                self.checks_collision(piecesBlack, pressed_square[0], pressed_square[1])
            elif current_piece[1].colour == 'black':
                self.collided = False
                self.checks_collision(piecesBlack, pressed_square[0], pressed_square[1])
                if self.collided:
                    self.move = False
                self.checks_collision(piecesWhite, pressed_square[0], pressed_square[1])

    def checks_collision(self,list,x,y):
        for i in range(0,len(list)):
            if (pygame.Rect(x,y,SquareWidth,SquareWidth)).colliderect(list[i][2]):
                self.collided = True
                self.j = i


class King:

    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.move = False
        self.collided = False

    def moving(self):
        if self.x != pressed_square[0] or self.y != pressed_square[1]:
            if self.x == pressed_square[0] or  self.x == (pressed_square[0]-SquareWidth) or self.x == (pressed_square[0]+SquareWidth):
                if self.y == pressed_square[1] or  self.y == (pressed_square[1]-SquareWidth) or self.y == (pressed_square[1]+SquareWidth):
                    self.move = True

        if self.move:
            if current_piece[1].colour == 'white':
                self.checks_collision(piecesWhite,pressed_square[0],pressed_square[1])
                if self.collided:
                    self.move = False
                self.checks_collision(piecesBlack,pressed_square[0],pressed_square[1])

            elif current_piece[1].colour == 'black':
                self.checks_collision(piecesBlack,pressed_square[0],pressed_square[1])
                if self.collided:
                    self.move = False
                self.checks_collision(piecesWhite,pressed_square[0],pressed_square[1])

        if pressed_square[1] == self.y: #this is for castling. the king is moving horizontally in line so y coordinate must stay the same
            if current_piece[1].colour == 'white':
                castle = self.castling(white_moved)
                return castle
            elif current_piece[1].colour == 'black':
                castle = self.castling(black_moved)
                return castle

    def checks_collision(self,list,x,y):
        for i in range(0,len(list)):
            if (pygame.Rect(x,y,SquareWidth,SquareWidth)).colliderect(list[i][2]):
                self.collided = True
                self.j = i

    def castling(self, moved_list): #this check which square is selected, if its one for castling then it checks if it can do that without collididng with anything, if yes then it returns the x coordiante the king should move to, otherwise it returns None. moved_list is eg white_moved, whoevers turns it is.
        if moved_list[1] == False:
            if pressed_square[0] == self.x+SquareWidth*2 or pressed_square[0]==self.x+SquareWidth*3: #if the king is going to go right then it moves to the right by two places.
                if moved_list[2] == False:
                    self.checks_collision(piecesWhite,self.x+SquareWidth, self.y)
                    self.checks_collision(piecesBlack,self.x+SquareWidth, self.y)
                    self.checks_collision(piecesWhite,self.x+2*SquareWidth, self.y)
                    self.checks_collision(piecesBlack,self.x+2*SquareWidth, self.y)
                    if self.collided == False:
                        self.move = True
                        new_king_pos = self.x+SquareWidth*2
                        return new_king_pos #returns the new x at which the king should be if it can castle
            elif pressed_square[0] == self.x-SquareWidth*2 or pressed_square[0] == self.x-SquareWidth*4: #if the king is going left then x will decrease by 2 squares/
                if moved_list[0] == False: #if left corner rook hasnt moved yet
                    for x in range(self.x-SquareWidth, self.x-SquareWidth*4, -SquareWidth): #checks collision between rook and king.
                        self.checks_collision(piecesBlack,x, self.y)
                        self.checks_collision(piecesWhite,x, self.y)
                    if self.collided == False:
                        self.move = True
                        new_king_pos = self.x-SquareWidth*2
                        return new_king_pos


for i in range(0,16): #creates all the pieces at the start of the game and stores them as object on the class Piece in two seperate array for the two colours
    piecesBlack[i][0] = pieces[i]
    piecesBlack[i][1] = Piece(piecesBlack[i][0], 'black')
    piecesBlack[i][2] = pygame.Rect([piecesBlack[i][1].x,piecesBlack[i][1].y, SquareWidth, SquareWidth])

    piecesWhite[i][0] = pieces[i]
    piecesWhite[i][1] = Piece(piecesWhite[i][0], 'white')
    piecesWhite[i][2] = pygame.Rect([piecesWhite[i][1].x,piecesWhite[i][1].y, SquareWidth, SquareWidth])


def main():
    displayingBoard() #function to draw the chess board onto the screen is called here


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        for i in range(0,2):
            if event.type == timers[i].timer_event:
                timers[i].timer_seconds -= 1

        if event.type == pygame.KEYUP:
            if event.key == 27:
                exit()


        if event.type == pygame.MOUSEBUTTONUP: #gets the coordinaets of where the mouse has been pressed
            mouse_pos = pygame.mouse.get_pos()

            if current_turn == 'white': #if its whites moves checks if the square pressed is white, if yes sets current_piece to the square, otherwise nothing happens. only once the current_piece is chosen, pressed_square an be chosen
                checking_move(piecesWhite, piecesBlack, mouse_pos)

            if current_turn == 'black':
                checking_move(piecesBlack, piecesWhite, mouse_pos)

            mouse_pos = []

    displaying_images() #draws the images of the pieces

    for i in range(0,2): #writing the timers every second
        timers[i].decreasing_timer()
        j = abs(i-1)

        writingText('time left:', (i*(PlayWidth+fromEdge_x)+100), (ScreenHeight*j-120*j+10), 200, 50, white, (j*999999999), 30)
        writingText(timers[i].timer, (i*(PlayWidth+fromEdge_x)+100), (ScreenHeight*j-120*j+60), 200, 50, white, (j*999999999), 30)

    if current_turn == 'white':
        pygame.draw.rect(screen, (255,0,0), ((0*(PlayWidth+fromEdge_x)+100), (ScreenHeight-110), 200, 100),5)
    else:
        pygame.draw.rect(screen, (255,0,0), ((1*(PlayWidth+fromEdge_x)+100), (10), 200, 100),5)

    #checking_king()
    pygame.display.flip()

'''
assigns_timers()

while True:
    main()
'''

import random
import pygame
import time

# GLOBALS VARS
s_width = 800
s_height = 800
play_width = 300  # meaning 300 // 5 = 60 width per block
play_height = 600  # meaning 600 // 10 = 60 height per block
block_size = 60
top_left_x = (s_width - play_width) // 2
top_left_y = (s_height - play_height) // 2

background_color = (169,169,169)
board_color = (0,0,0)

code_length = 4
pegs = [1,2,3,4,5,6]

c1 = (239, 70, 95) #crimson
c2 = (255,140,0) #dark orange
c3 = (255,255,0) #yellow
c4 = (154,205,50) # yellow green
c5 = (30,144,255) # dodger blue
c6 = (200,112,219) #med purple
colors = { 'R' : c1, 'O' : c2, 'Y' : c3, 'G' : c4, 'B' : c5, 'P' : c6}

####from console verion
def generateCode():
    code = []
    for i in range(code_length):
        code.append(random.choice(pegs))
    return code

def checkWin(score):
    sum = 0
    for x in range(code_length):
        sum += score[x]
    if sum ==8:
        return True
    return False

def evaluate(c, guess):
    code = c.copy()
    score = []
    
    #allocate white pegs
    for x in range(code_length):
        try:
            if code[x] == int(guess[x]):
                code[x] = -1
                score.append(2)
        except: 
            exit

    #allocate red pegs
    for x in range(code_length):
        try:
            if int(guess[x]) in code:
                code.remove(int(guess[x]))
                code.append(-1)
                score.append(1)
        except: 
            exit

    #fill rest of score with blank pegs
    while len(score) < 4:
        score.append(0)
    return score

####new for interface version 


def button(text,  pos, color):
    font = pygame.font.SysFont("Arial", 20)
    text_render = font.render(text, 1, (0, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = pos
    pygame.draw.circle(win, color, pos, 25)
    return win.blit(text_render, (x - block_size//8, y - block_size//6))


def makeButtons():
    bs = []
    spacingX = s_width // (len(pegs) + 1)
    h = 750
    i = 0
    for x,y in colors.items():
        b = button(x, ((i + 1)*spacingX - (block_size/3), h), y)
        bs.append(b)
        i += 1
    return bs

def lostGame():
    font = pygame.font.SysFont('comicsans', 150)
    label = font.render('You lost', 1, (0,0,255))
    win.blit(label, ((s_width - label.get_width())/2, (s_height - label.get_height()) /2))
    pygame.display.update()

def wonGame():
    font = pygame.font.SysFont('comicsans', 150)
    label = font.render('You win!', 1, (0,255,0))
    win.blit(label, ((s_width - label.get_width())/2, (s_height - label.get_height()) /2))
    pygame.display.update()    

def updateScore(turn, turnScore):
    radius = block_size/4 - 5
    #draw quadrant in score col with red, white, or black 
    #coordinate of score box is 
        #x = top_left_x -> + block_size
        # y = 
    peg0 = (top_left_x + block_size/4, top_left_y + block_size/4 + (play_height/10)*(11-turn))
    peg1 = (top_left_x + block_size/2 + block_size/4, top_left_y+ block_size/4 + (play_height/10)*(11-turn))
    peg2 = (top_left_x+ block_size/4, top_left_y+ block_size/4 + block_size/2 + (play_height/10)*(11-turn))
    peg3 = (top_left_x+ block_size/4 + block_size/2, top_left_y + block_size/4+ block_size/2 + (play_height/10)*(11-turn))

    if turnScore[0] == 2:
        pygame.draw.circle(win, (255,255,255), peg0, radius)
    elif turnScore[0] == 1:
        pygame.draw.circle(win, (255,20,0), peg0, radius)
    else:
        pygame.draw.circle(win, (96,96,96), peg0, radius) 

    if turnScore[1] == 2:
        pygame.draw.circle(win, (255,255,255), peg1, radius)
    elif turnScore[1] == 1:
        pygame.draw.circle(win, (255,20,0), peg1, radius)
    else:
        pygame.draw.circle(win, (96,96,96), peg1, radius)  
    
    if turnScore[2] == 2:
        pygame.draw.circle(win, (255,255,255), peg2, radius)
    elif turnScore[2] == 1:
        pygame.draw.circle(win, (255,20,0), peg2, radius)
    else:
        pygame.draw.circle(win, (96,96,96), peg2, radius)  

    if turnScore[3] == 2:
        pygame.draw.circle(win, (255,255,255), peg3, radius)
    elif turnScore[3] == 1:
        pygame.draw.circle(win, (255,20,0), peg3, radius)
    else:
       pygame.draw.circle(win, (96,96,96), peg3, radius)  

    pygame.display.update()
    exit

def updateGuess(turn, g):
    length = len(g)
    guess = list(g)
    peg0 = (top_left_x + (block_size)*(length) + block_size/2, top_left_y + (play_height/10)*(10-turn) + block_size/2)
    i = 1
    for x, y in colors.items():
        if int(guess[length - 1]) == i:
            color = y
        i += 1
    #pygame.draw.rect(win, color, peg0)
    pygame.draw.circle(win, color, peg0, block_size/2 - 5)
    pygame.display.update()

def create_grid():
    #creates a 5x10 grid of black
    grid = [[background_color for _ in range(5)] for _ in range(10)]

    for i in range(len(grid)):
        for k in range(len(grid[i])):
            grid[i][k] = board_color
    return grid

def draw_window():
    win.fill(background_color)
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 45)
    label = font.render("MasterMind", 1, (255,255,255))

    win.blit(label, (s_width / 2 - (label.get_width() / 2), 45))

    #draw the board
    grid = create_grid()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(win, grid[i][j], (top_left_x + j*block_size, top_left_y + i * block_size, block_size, block_size), 0)
    #draw board border 
    pygame.draw.rect(win, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height), 2)
    
    draw_rows(grid)
    pygame.draw.line(win, (255, 255, 255), (top_left_x + block_size, top_left_y), (top_left_x + block_size, top_left_y + play_height))

    pygame.draw.rect(win, background_color, (top_left_x, top_left_y, play_width + 2, block_size))

    pygame.display.update()
    
def draw_rows(grid):
    sx = top_left_x 
    sy = top_left_y

    for i in range(len(grid)):
        #draw row dividers
        pygame.draw.line(win, (255, 255, 255), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))


def main():
    
    draw_window()
    buttons = makeButtons()
    pygame.display.update()
    turn = 1
    guessedRight = False
    code = generateCode()
    guess = ""

    while not guessedRight and turn < 10:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.collidepoint(pygame.mouse.get_pos()):
                        if len(guess) < 4:
                            if buttons.index(b) == 0:
                                guess += '1'
                            elif buttons.index(b) == 1:
                                guess += '2'
                            elif buttons.index(b) == 2:
                                guess += '3'
                            elif buttons.index(b) == 3:
                                guess += '4'
                            elif buttons.index(b) == 4:
                                guess += '5'
                            elif buttons.index(b) == 5:
                                guess += '6'
                        updateGuess(turn, guess)
                
        if len(guess) == 4:
            turnScore = evaluate(code, list(guess))
            turn += 1
            updateScore(turn, turnScore)
            guess = ''
            #check if player won
            if checkWin(turnScore):
                wonGame()
                return
            

    if turn == 10:
        lostGame()
    
pygame.init()
win = pygame.display.set_mode(((s_width, s_height)))
pygame.display.set_caption('MasterMind')
main()
time.sleep(5)
"""
Austin Beard Matching Game
"""
import pygame, random


pygame.init()

#screen
WIDTH = 600
HEIGHT = 600

#colors
blue = (128, 128, 128)
white = (255, 255, 255)
black = (0, 0, 0)
red = (0, 0, 225)
green = (0, 255, 0)


#game board
rows = 6
cols = 8
correct = [[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]]
options = []
blank = []
used = []
newBoard = True
firstGuess = False
secondGuess = False
firstNum = 0
secondNum = 0
turn = 0
highScore = 0
matches = 0
gameOver = False

# create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Matching Game')
titleFont = pygame.font.Font('bubble.ttf', 46)
smallFont = pygame.font.Font('roboto.ttf', 26)


def randPlacement():
    global options, blank, used
    
    for item in range(rows * cols // 2):
        options.append(item)

    for item in range(rows * cols):
        piece = options[random.randint(0, len(options) - 1)]
        blank.append(piece)
        if piece in used:
            used.remove(piece)
            options.remove(piece)
        else:
            used.append(piece)


def getBoard():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, 100])
    title = titleFont.render('    Match The Numbers!', True, white)
    screen.blit(title, (10, 5))
    pygame.draw.rect(screen, black, [0, 100, WIDTH, HEIGHT - 200], 0)
    pygame.draw.rect(screen, black, [0, HEIGHT - 100, WIDTH, 100], 0)
    restartButton = pygame.draw.rect(screen, black, [10, HEIGHT - 90, 200, 80], 0, 5)
    restartLabel = titleFont.render('Restart', True, white)
    screen.blit(restartLabel, (10, 520))
    scoreLabel = smallFont.render(f'Turns: {turn}', True, white)
    screen.blit(scoreLabel, (20, 70))
    highscoreLabel = smallFont.render(f'High Score: {highScore}', True, white)
    screen.blit(highscoreLabel, (400, 70))
    return restartButton




def checkBoard():
    global rows, cols, correct
    
    boardList = []
    for i in range(cols):
        for j in range(rows):
            piece = pygame.draw.rect(screen, blue, [i * 75 + 12, j * 65 + 112, 50, 50], 0, 4)
            boardList.append(piece)

    for r in range(rows):
        for c in range(cols):
            if correct[r][c] == 1:
                pygame.draw.rect(screen, green, [c * 75 + 10, r * 65 + 110, 54, 54], 3, 4)
                pieceText = smallFont.render(f'{blank[c * rows + r]}', True, black)
                screen.blit(pieceText, (c * 75 + 18, r * 65 + 120))

    return boardList


def checkGuess(first, second):
    global blank, correct, turn, matches
    
    if blank[first] == blank[second]:
        col1 = first // rows
        col2 = second // rows
        row1 = first - (first // rows * rows)
        row2 = second - (second // rows * rows)
        if correct[row1][col1] == 0 and correct[row2][col2] == 0:
            correct[row1][col1] = 1
            correct[row2][col2] = 1
            turn += 1
            matches += 1
    else:
        turn += 1


running = True
while running:
    
    screen.fill(white)
    if newBoard:
        randPlacement()
        newBoard = False
    restart = getBoard()
    board = checkBoard()

    if firstGuess and secondGuess:
        checkGuess(firstNum, secondNum)
        pygame.time.delay(1000)
        firstGuess = False
        secondGuess = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(board)):
                button = board[i]
                if not gameOver:
                    if button.collidepoint(event.pos) and not firstGuess:
                        firstGuess = True
                        firstNum = i
                    if button.collidepoint(event.pos) and not secondGuess and firstGuess and i != firstNum:
                        secondGuess = True
                        secondNum = i
            if restart.collidepoint(event.pos):
                options = []
                used = []
                blank = []
                newBoard = True
                turn = 0
                matches = 0
                firstGuess = False
                secondGuess = False
                correct = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
                gameOver = False


    if matches == rows * cols // 2:
        gameOver = True
        winner = pygame.draw.rect(screen, black, [10, HEIGHT - 300, WIDTH - 20, 80], 0, 5)
        winnerText = titleFont.render(f'You Won in {turn} moves!', True, white)
        screen.blit(winnerText, (10, HEIGHT - 300))
        if highScore > turn or highScore == 0:
            highScore = turn


    if firstGuess:
        pieceText = smallFont.render(f'{blank[firstNum]}', True, red)
        location = (firstNum // rows * 75 + 18, (firstNum - (firstNum // rows * rows)) * 65 + 120)
        screen.blit(pieceText, (location))

    if secondGuess:
        pieceText = smallFont.render(f'{blank[secondNum]}', True, red)
        location = (secondNum // rows * 75 + 18, (secondNum - (secondNum // rows * rows)) * 65 + 120)
        screen.blit(pieceText, (location))

    pygame.display.flip()
pygame.quit()
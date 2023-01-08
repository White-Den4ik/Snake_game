import pygame
import time
import random

pygame.init()

# COLOURS R   G   B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREEN = (0, 155, 0)
AQUA = (0, 255, 255)
ORANGE = (180, 102, 0)

img_SnakeHead = pygame.image.load("SnakeHead.png")
img_Cherry = pygame.image.load("cherry.png")
img_Icon = pygame.image.load("icon_snake.png")

# Игровое окно
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Змейка")
pygame.display.set_icon(img_Icon)

pygame.display.update()

clock = pygame.time.Clock()
fps = 30


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if event.type == pygame.TEXTINPUT:
            if event.text == "e":
                intro = False
            if event.text == "q":
                pygame.quit()
                quit()

        gameDisplay.fill(WHITE)
        message_to_screen("Добро пожаловать в Змейку!",
                          colour=BLUE,
                          y_displace=-100,
                          size="large")
        message_to_screen("Цель игры - съесть яблоко, которое появляется на экране.",
                          colour=BLACK,
                          y_displace=-30)
        message_to_screen("Чем больше яблок ты съешь, тем длинее ты станешь.",
                          colour=BLACK,
                          y_displace=10)
        message_to_screen("Если ты ударишься о границы игры или по себе, ты проиграешь.",
                          colour=BLACK,
                          y_displace=50)
        message_to_screen("Нажми E чтобы начать игру, SPACE для паузы и Q чтобы выйти.",
                          colour=DARKGREEN,
                          y_displace=150)

        pygame.display.update()
        clock.tick(15)


# Пауза
def pause():
    paused = True

    message_to_screen("Пауза",
                      BLUE,
                      -100,
                      size="large")

    message_to_screen("Нажмите E чтобы продолжить игру или Q для выхода",
                      BLACK,
                      25)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(15)


# Счет
def score(score):
    text = medfont.render("Счет: " + str(score), True, BLACK)
    gameDisplay.blit(text, [12, 12])


# Координаты яблок
def randAppleGen(borderSize, objectSize):
    randAppleX = round(random.randrange(borderSize, display_width - (objectSize + borderSize)))
    randAppleY = round(random.randrange(borderSize, display_height - (objectSize + borderSize)))

    return randAppleX, randAppleY


# Змея
direction = 'right'


def snake(lead_width, lead_height, snakeList):
    if direction == 'right':
        head = pygame.transform.rotate(img_SnakeHead, 270)

    if direction == 'left':
        head = pygame.transform.rotate(img_SnakeHead, 90)

    if direction == 'up':
        head = img_SnakeHead

    if direction == 'down':
        head = pygame.transform.rotate(img_SnakeHead, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, DARKGREEN, [XnY[0], XnY[1], lead_width, lead_height])


smallfont = pygame.font.SysFont("arialms", 25)
medfont = pygame.font.SysFont("bahnschrift", 50)
largefont = pygame.font.SysFont("comicsansms", 50)


def text_objects(text, colour, size):
    if size == "small":
        textSurface = smallfont.render(text, True, colour)
    elif size == "medium":
        textSurface = medfont.render(text, True, colour)
    elif size == "large":
        textSurface = largefont.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, colour, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    gameExit = False
    gameOver = False

    lead_width = 20
    lead_height = 20
    lead_x_change = 1
    lead_y_change = 0
    lead_x = display_width / 2
    lead_y = display_height / 2
    block_change = 10
    border = 10
    snakeList = []
    snakeLength = 1
    appleThickness = 20
    global direction

    randAppleX, randAppleY = randAppleGen(border, appleThickness)

    while not gameExit:

        if gameOver == True:
            message_to_screen("Игра окончена",
                              BLUE,
                              y_displace=-50,
                              size="large")
            message_to_screen("Нажмите E чтобы продолжить игру или Q для выхода.",
                              BLACK,
                              y_displace=+50,
                              size="small")
            pygame.display.update()

        while gameOver == True:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_e:
                        direction = 'right'
                        gameLoop()
                elif event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    if direction == 'right':
                        continue
                    lead_x_change = -block_change
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    if direction == 'left':
                        continue
                    lead_x_change = block_change
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    if direction == 'down':
                        continue
                    lead_y_change = -block_change
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    if direction == 'up':
                        continue
                    lead_y_change = block_change
                    lead_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_SPACE:
                    pause()

            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True

        if lead_x >= display_width - lead_width or lead_x <= 0 or lead_y >= display_height - lead_height or lead_y <= 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(ORANGE)
        pygame.draw.rect(gameDisplay, BLACK, [0, 0, display_width, display_height], border)
        gameDisplay.blit(img_Cherry, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(lead_width, lead_height, snakeList)

        score(snakeLength - 1)

        if lead_x >= randAppleX and lead_x <= randAppleX + appleThickness or lead_x + block_change >= randAppleX and lead_x + block_change <= randAppleX + appleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen(border, appleThickness)
                snakeLength += 1
            elif lead_y + block_change >= randAppleY and lead_y + block_change <= randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen(border, appleThickness)
                snakeLength += 1

        pygame.display.update()

        clock.tick(fps)

    pygame.display.update()

    pygame.quit()
    quit()


game_intro()
gameLoop()

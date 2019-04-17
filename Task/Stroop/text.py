import sys
import time
import pygame



pygame.init()
###전역 변수
## 초당 프레임수를 정의
TARGET_FPS = 30

##색 변수
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
GREEN = (0,255,0)
RED   = (255,0,0)
RED_A = (255,0,0,127) #희미한 빨강 -> 255 완전 불투명

## screen 정의
SIZE = width, height = [1800,600]
CENTER = (width/2, height/2)

## 마우스 버튼 인덱스 정의
LEFT = 1  # 왼쪽 버튼에 대한 버튼 인덱스
RIGHT = 3  # 오른쪽 버튼에 대한 버튼 인덱스

screen = pygame.display.set_mode(SIZE) ##pygame.FULLSCREEN | HWSURFACE | OPENGL or DOUBLEBUF
pygame.display.set_caption("STROOP")
clock = pygame.time.Clock()

#def printText(msg, color = "WHITE", pos=(50, 50)):
done = False
flag = None
font = pygame.font.SysFont("consolas", 20)
textSurface = font.render(msg, True, pygame.Color(color), None)
textRect = textSurface.get_rect(Lefttop = (900, 300))

screen.blit(textSurface, textRect)

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            buttons = [pygame.key.name(k) for k,v in enumerate(pressed) if v]
            flag = True
        elif event.type == pygame.KEYUP:
            flag = False
        elif event.type == pygame.QUIT:
            done = True
    
    screen.fill(BLACK)
    clock.tick(TARGET_FPS)

    if flag == True:
        printText('아 왤케 안되냐', 'WHITE')
        printText('아 왤케 안되냐' + buttons[0], 'WHITE')
    elif flag == False:
        printText('미치겠네', 'WHITE')
    else:
        printText('버튼을 누르시오')
    
    pygame.display.flip()
        


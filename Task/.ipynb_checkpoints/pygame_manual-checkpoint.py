import sys
import time
import pygame

###전역 변수
## 초당 프레임수를 정의
TARGET_FPS = 30
 
clock = pygame.time.Clock()

##스피드(ex. ball 5 종류의 스피드)
#SPEED = [1,2,4,8,16]


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

##사각형 정의?????
#rectangle = (0, 10, 100, 100)  # 왼쪽 X, 위 Y, 너비, 높이

## 마우스 버튼 인덱스 정의
LEFT = 1  # 왼쪽 버튼에 대한 버튼 인덱스
RIGHT = 3  # 오른쪽 버튼에 대한 버튼 인덱스

## pygame 시작
pygame.init()

##화면 세팅
screen = pygame.display.set_mode(SIZE) ##FULLSCREEN | HWSURFACE | OPENGL or DOUBLEBUF

##GUI 창 이름
pygame.display.set_caption("STROOP")

##이미지 불러오기
#ball = pygame.image.load("C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfotnothing/OBELAB/intro_ball.gif")

##obj 범위????
#ballrect = ball.get_rect()

## 도형 코딩
'''
polygon = pygame.draw.polygon() # 다각형 pygame.draw.polygon('화면', '색상', [좌표], 선굵기(0은 채우기))
rect = pygame.draw.rect() # 사각형 pygame.draw.rect('화면', '색상', (왼쪽, 위, 너비, 높이 순), 선굵기(0은 채우기))
circle = pygame.draw.circle() #원 pygame.draw.circle('화면', '색상', [좌표], 반지름, 선굵기(0은 채우기))
ellipse = pygame.draw.ellipse() #타원 pygame.draw.ellipse('화면', '색상', [좌표], 선굵기(0은 채우기))
line = pygame.draw.line() #선 pygame.draw.line('화면', '색상', [시작 좌표], [끝 좌표], 선굵기(0은 채우기))
lines = pygame.draw.lines() #다중 선 pygame.draw.lines('화면', '색상', closed, [좌표], 선굵기(0은 채우기))
aaline = pygame.draw.aaline() #부드러운 선 pygame.draw.aaline('화면', '색상', [시작 좌표], [끝 좌표], 선굵기(0은 채우기), Blend(True | False))
aalines = pygame.draw.aalines() #부드러운 다중 성 pygame.draw.aalines('화면', '색상', closed, [좌표], 선굵기(0은 채우기), Blend(True | False))
'''


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not hasattr(event, 'key'):
            continue
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:

##기본 키 세팅
'''
        if not hasattr(evenet, 'key'):
            continue
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
            elif event.key == K_LEFT:
            elif event.key == K_UP:
            elif event.key == K_DOWN:

##마우스 이벤트

    if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
        # 왼쪽 버튼이 눌렸을 때의 처리
        print "left mouse up (%d, %d)" % event.pos
    elif event.type == MOUSEBUTTONUP and event.button == LEFT:
        # 왼쪽 버튼이 떨어졌을 때의 처리
        print "left mouse down (%d, %d)" % event.pos
    elif event.type == pygame.MOUSEMOTION:
        # 마우스 이동시의 처리
        print "mouse move (%d, %d)" % event.pos


'''
##screen cleaner
pygame.draw.rect(screen, GREEN, [10, 10, 100, 100], 0)

screen.fill(BLACK)

## 사각형 생성
'''
rect = box.get_rect()
rect.center =(CENTER)
screen.blit(box, rect)
'''
## 소환된 이미지를 화면에 표현
pygame.display.flip()

clock.tick(TARGET_FPS)


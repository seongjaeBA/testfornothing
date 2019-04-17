import sys
import pygame

## pygame 시작
pygame.init()

##전역 변수
speed = [2,2]
black = (0, 0, 0)

##화면 세팅
size = width, height = [1800,600]
screen = pygame.display.set_mode(size)

##obj  세팅
ball = pygame.image.load("C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfotnothing/OBELAB/intro_ball.gif")

##obj 범위????
ballrect = ball.get_rect()

##GUI 창 이름
pygame.display.set_caption("제목")


## 예제 게임
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    ##RGB 값
    screen.fill(black) # blacl = 0, 0, 0

    ## surface.blit() 을 통해서 버퍼에 이미지 소환
    screen.blit(ball, ballrect)

    ## 소환된 이미지를 화면에 표현
    pygame.display.flip()

    
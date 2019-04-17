import pygame as pg

## pygame 시작
pg.init()

##전역 변수
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

##화면 세팅
SIZE = width, height = [400,300]
screen = pg.display.set_mode(SIZE)

##GUI 창 이름
pg.display.set_caption("제목")

## 쉬운 코딩을 위한 작업.
done = False ## 게임 전원

clock = pg.time.Clock() ## 구현 시간 frame 초당 x번

while not done:
    clock.tick(10)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
              
    ##RGB 값
    screen.fill(WHITE)

    pg.draw.polygon(screen, GREEN, [[30, 150], [125, 100], [220, 150]], 5)
    pg.draw.polygon(screen, GREEN, [[30, 150], [125, 100], [220, 150]], 0)
    pg.draw.lines(screen, RED, False, [[50, 150], [50, 250], [200, 250], [200, 150]], 5)
    pg.draw.rect(screen, BLACK, [75, 175, 75, 50], 5)
    pg.draw.rect(screen, BLUE, [75, 175, 75, 50], 0)
    pg.draw.line(screen, BLACK, [112, 175], [112, 225], 5)
    pg.draw.line(screen, BLACK, [75, 200], [150, 200], 5)

    ## 소환된 이미지를 화면에 표현
    pg.display.flip()

    
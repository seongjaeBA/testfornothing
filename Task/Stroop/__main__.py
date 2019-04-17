import sys
import pygame
import time
import datetime
import csv
import OBELAB.Stroop
from OBELAB.Stroop import stroop

##전역 변수
## 시간 가져오기
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
'''

    with open('stroop_'+ /d/d +'csv' %% id, datetime, w, encoding = utf8) as data:
        
        writer = csv.writer(data)
        for row in rows:
            writer.writerow(row)

    data.close()
'''
#색 변수
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
GREEN = (0,255,0)
RED   = (255,0,0)
RED_A = (255,0,0,127) #희미한 빨강 -> 255 완전 불투명

## 화면 크기

screen_size = (1800, 600) #임의 화면 크기 display 크기 가져와야 할듯

def submit(ID, Trial): ## 아이디, 시행 등록 
    
def printText() ## 텍스트 구현 환경 설정

def stimulis() ## 자극 설정

def initTask()  ## 환경 설정
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Stroop')
    clock = pygame.time.Clock()
    ### play 

def runTask() ## 과제 실행
    clock.tick(30) # 프레임 설정
    done = False 
    flag1, flag2, flag3 = None

    while not done:  ##과제 시행


if __name__ == "__main__":
    initTask()
    pygame.quit()
    sys.exit()



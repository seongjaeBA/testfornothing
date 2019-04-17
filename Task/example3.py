# Import a library of functions called 'pygame'
import pygame
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
 
# Set the height and width of the screen
size   = (400, 300)

# print text function
def printText(msg, color='BLACK'):
    textSurface      = font.render(msg, True, pygame.Color(color), None)
    textRect         = textSurface.get_rect()
    textRect.center = (size[0]/2, size[1]/2)
 
    screen.blit(textSurface, textRect)

def runTask():
    global screen, clock, font
    #Loop until the user clicks the close button.
    done  = False
    flag  = None

    while not done:
    
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)
        
        # Main Event Loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.MOUSEMOTION: # If user release what he pressed.
                flag = True
            elif event.type == pygame.QUIT:  # If user clicked close.
                done = True                 
    
        
        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
        
        # Clear the screen and set the screen background
        screen.fill(WHITE)
        
    
        # Print red text if user pressed any key.
        if flag == True:
            printText('OBELAB', 'BLUE')
            flag = False
    
        # Print blue text if user released any key.
        elif flag == False:
            printText('Your mouse is now stopped!!', 'BLUE')
    
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
 

def initTask():
    global screen, clock, font

    pygame.init()
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("consolas", 20)
    pygame.display.set_caption("Game Title")
    
    clock = pygame.time.Clock()
    runTask()

# Be IDLE friendly
if __name__ == '__main__':
    initTask()
    pygame.quit()
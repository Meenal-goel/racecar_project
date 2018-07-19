import pygame
import time
import random

score = 0
pygame.init() #initiate pygame and all the modules present within it

crash_sound = pygame.mixer.Sound("F:/car race game/music/Crash.wav")
pygame.mixer.music.load("F:/car race game/music/Race_Car.wav")
click_sound = pygame.mixer.Sound("F:/car race game/music/button-3.wav")
key_sound = pygame.mixer.Sound("F:/car race game/music/left.wav")
#setting the screen dimensions
display_width = 600
display_height = 400

gameDisplay = pygame.display.set_mode((display_width, display_height))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_green = (178, 255, 102)
light_red = (255, 102, 102)

car_width = 60

pygame.display.set_caption('Raging Motor')

clock = pygame.time.Clock()

carImg = pygame.image.load('F:/car race game/images/car.png')
smashedImg = pygame.image.load('F:/car race game/images/smash.png')
gameIcon = pygame.image.load('F:/car race game/images/gameicon.png')

pygame.display.set_icon(gameIcon)


#function to display the barriers escaped
def barrier_count(escaped):
    font =  pygame.font.SysFont('lilyupc',30)
    text = font.render("Barriers escaped:"+str(escaped),True,black)
    gameDisplay.blit(text,[1,1])

def score_fun(score):

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    appearText = pygame.font.SysFont('palatinolinotype',50)
    TextSurf,TextRect = text_obj("SCORE : "+str(score), appearText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(3)
    car_bump()

#function to set barriers in the game
def barrier(bx, by, bw, bh, color):
    pygame.draw.rect(gameDisplay, color, [bx, by, bw, bh])
    

#function to provide car positioning coordinates
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def dest_car(x,y):
    gameDisplay.blit(smashedImg, (x,y))


#function to render the text based upon surface
def text_obj(text,font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()

#function to manage display text style
def crash_msg(text):
    appearText = pygame.font.SysFont('arialms.tff',100)
    TextSurf,TextRect = text_obj(text, appearText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()
    
    #the message will be displayed for the specified time (4 sec here)
    time.sleep(1)

   #call function to start again
    game_StartAgain()



#function to display message when car crashes
def car_bump():

    gameDisplay.fill(white)      
    crash_msg("CAR SMASHED")
   
    
    
#function to set buttons on start of game       
def displayButtons(msg, x, y, w, h, active_colr, inactive_colr, action):
    
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        

        #mentioning boundaries of box buttons
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
             pygame.draw.rect(gameDisplay, active_colr, [x, y, w, h])
             if click[0] == 1 and action != None:
                 pygame.mixer.Sound.play(click_sound)
                 action()
                      
        else:   
             pygame.draw.rect(gameDisplay, inactive_colr, [x, y, w, h])

        buttonText = pygame.font.SysFont("arialms",20)
        TextSurf,TextRect = text_obj(msg, buttonText)
        TextRect.center = ((x+w/2), (y+h/2))
        gameDisplay.blit(TextSurf,TextRect)

#function to start over
def game_StartAgain():
  
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_fun()
        gameDisplay.fill(white)
        appearText = pygame.font.SysFont('arialms',60)
        TextSurf,TextRect = text_obj(" Oops! Make A Choice ", appearText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf,TextRect)

        displayButtons("Try Again", 150, 250, 100, 50, green, light_green,game_Logic)
        displayButtons("Leave", 350, 250, 100, 50, red, light_red, exit_fun)

        pygame.display.update()
        clock.tick(10)

#function to unpause
def unpause_game():
    global pause
    pygame.mixer.music.unpause()
    pause = False

            
#function to pause the game
def game_Pause():
    
    pygame.mixer.music.pause()
   
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_fun()
        gameDisplay.fill(white)

        appearText = pygame.font.SysFont('arialms',90)
        TextSurf,TextRect = text_obj("PAUSED", appearText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf,TextRect)

        displayButtons("Continue", 150, 250, 100, 50, green, light_green,unpause_game)
        displayButtons("Quit", 350, 250, 100, 50, red, light_red, exit_fun)

        pygame.display.update()
        clock.tick(10)

#function introducing game
def game_Abstract():

    abstract = True
    while abstract:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_fun()
        gameDisplay.fill(white)

        appearText = pygame.font.SysFont('informalroman',100)
        TextSurf,TextRect = text_obj("Raging Moto", appearText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf,TextRect)

        displayButtons("Let's Start", 150, 260, 100, 50, green, light_green,game_Logic)
        displayButtons("Say Bye", 350, 260, 100, 50, red, light_red, exit_fun)

        pygame.display.update()
        clock.tick(10)

#function to exit
def exit_fun():
    pygame.quit()
    quit()

        

#function containing main logic behind the car movement
def game_Logic():
    
    global pause

    #play music infinite times
    pygame.mixer.music.play(-1)
    #setting the initial position of the car
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    #setting the initial change in state zero because no key is pressed
    x_move = 0

    #setting the variables for barrier function to work
    barrier_beginx = random.randrange(0,display_width)
    barrier_beginy = -600
    barrier_speed = 2
    barrier_width = 80
    barrier_height = 80
    barrier_color = blue

    score = 0 
    escaped = 0
    

    raceExit= False #we have not exit,if true we need to do something

    #until we exit
    while not raceExit:

        for event in pygame.event.get():  #get any event done by user-key press,mouse hover etc

            if event.type == pygame.QUIT:
                #stop pygame
                exit_fun()
                               

            if event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(key_sound)
                if event.key == pygame.K_LEFT:
                    x_move = -5
                if event.key == pygame.K_RIGHT:
                    x_move = 5
                if event.key == pygame.K_p:
                    pygame.mixer.Sound.play(click_sound)
                    pause =True
                    game_Pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

        x += x_move
        
        #displaying bg in white color            
        gameDisplay.fill(white)        

        barrier(barrier_beginx,barrier_beginy,barrier_width,barrier_height,barrier_color)
        barrier_beginy += barrier_speed
        
        #placing car over the white display
        car(x,y)

        #calling function to count barriers escaped
        barrier_count(escaped)


        #conditional statements to manage the boundary 
        if x > display_width - car_width or x < 0:
             dest_car(x,y)
             score_fun(score)
             
             
                     
        if barrier_beginy > display_height:
            barrier_beginy = 0 - barrier_height
            barrier_beginx = random.randrange(0, display_width)
            #counter to increase barrier escaped
            escaped += 1
            score += 1
            #increase difficulty - increasing speed and barrier size
            barrier_speed += 1 
            barrier_width += 2
        
        #barrier-car y cross-over
        if y < barrier_beginy + barrier_height:
            
            #barrier-car x cross-over(checking if car is present within barrier boundaries)
            if x > barrier_beginx and x < barrier_beginx + barrier_width or x + car_width > barrier_beginx and x + car_width < barrier_beginx + barrier_width:
                dest_car(x,y)
                score_fun(score)
                
        
        pygame.display.update() #used to update the display after each event occurs

        clock.tick(80) #moving frames per second(managing car speed)
        

game_Abstract()
game_Logic()
exit_fun()

5#PROJECT GEIMU ALPHA VER 4.1 - more blocks and stuff
import os, sys, time
import pygame
from pygame.locals import *
from Player import Player
from enum import Enum
from Level import *
from datetime import datetime

print("Running")
class MainGame:
    gameDisplay = None
    quit_ = False
    crashed = False
    def __init__(self, windWidth = 800, windHeight = 600):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((windWidth, windHeight))
        #pygame.key.set_repeat(50,10)
        pygame.mixer.init()
        pygame.mixer.music.load("resources/music/track1.mp3")
        pygame.mixer.music.set_volume(0.5)
    def __del__(self):
        pygame.display.quit()
        pygame.mixer.music.stop()
    def isCrashed(self):
        return self.crashed
    def isQuit(self):
        return self.quit_
    def crashGame(self):
        self.crashed = True
        return
    def quitGame(self):
        print("Received gameQuit message")
        self.quit_ = True
        return
    def getClock(self):
        return self.gameClock

mainGame = MainGame(1024,768)
#GLOBALS
X = 0
Y = 1
groundPos = 450 # global temporary variable (useless once collision is implemented) ; might use this for a global death barrier (below screen)
_fps = 120
WIND_WIDTH = 1024
WIND_HEIGHT = 768
HALF_WIDTH = 512
HALF_HEIGHT = 384

##cameraXPOS = 0 # failed idea
##cameraYPOS = 0

#DEBUGGING
font = pygame.font.Font(None, 20)
fontSpace = 12

def sPrint(val, x, y):
    mainGame.gameDisplay.blit(font.render(str(val), 0, (0,0,0)),(x,y)) 

def cap(maxVal, eq): # caps a value to prevent an equation from breaking said cap ; global function
    if abs(eq) > abs(maxVal):
        return maxVal
    return eq

'''
def scrollCamera(player):
    global cameraXPOS
    global cameraYPOS
    if player.getPos()[X] < HALF_WIDTH - 100:
        cameraXPOS = cameraXPOS + 5
    elif player.getPos()[X] > HALF_WIDTH + 100:
        cameraXPOS = cameraXPOS - 5

    if player.getPos()[Y] < groundPos - 6:
        cameraYPOS =  cameraYPOS - 5
    elif player.getPos()[Y] > groundPos - 6:
        cameraYPOS = cameraYPOS + 5
'''

#BEGIN INIT BLOCK




#PLAYER STUFF
player_ = Player(50,640)
hitBoxRect = player_.rect.copy()
hitBoxRect.width /= 2
hitBoxRect.height /= 2
hitBoxRect.center = player_.rect.center # this is a smaller box inside the player thats half the players size which will handle our logical collisions

#SCENE
levelCode = 1
soloEntity = pygame.sprite.OrderedUpdates() # player sprite group
entities = pygame.sprite.OrderedUpdates() # uhh
entities2 = pygame.sprite.OrderedUpdates() # built in functions to draw objects with my velocity calculations ; special type of sprite goup that makes sure there is order to updating objects contained within

level_ = Level(levelCode,entities2)


testRects = [
    Block(Rect(530,305,100,100),"1", BlockType.HYBRID,(0,0,0),True),
    Block(Rect(-100,groundPos+20,1000,10),"2", BlockType.GROUND,(0,0,0),True),
    Block(Rect(395,0,10,265),"3", BlockType.WALL,(0,0,0),True),
    Block(Rect(470,groundPos-200,10,150),"4", BlockType.WALL,(0,0,0),True),
    Block(Rect(500,groundPos-195,180,10),"5", BlockType.GROUND,(0,0,0),True),
    Block(Rect(100,groundPos-20,200,10),"6", BlockType.GROUND,(0,0,0),True),
    Block(Rect(395,315,10,120),"3", BlockType.WALL,(0,0,0),True),
] 
specialRects = [Block(Rect(-5,0,10,groundPos+30),"7", BlockType.SPECIAL,(0,0,0),True),
                Block(Rect(795,0,10,groundPos+30),"8", BlockType.SPECIAL,(0,0,0),True)] 
for i in testRects:
    entities.add(i)
soloEntity.add(player_) # we add items to the entities object so we can draw everything with one function call
for i in specialRects: # print these in front of the player
    entities.add(i)

#SYSTEM
JUMP_KEY = pygame.K_z # jump key
ALT_JUMP_KEY = pygame.K_UP
RESET_POS = pygame.K_y # debug key
DASH_KEY = pygame.K_c # dash key
ALT_DASH_KEY = pygame.K_SPACE

#SOUND
pygame.mixer.music.play(-1)
jumpSound = pygame.mixer.Sound("resources/sound/JUMP.wav")
jumpSound.set_volume(0.5)
dashSound = pygame.mixer.Sound("resources/sound/dash.wav")

#END INIT BLOCK

startTime = datetime.now()
while not mainGame.isCrashed() and not mainGame.isQuit():
    pygame.time.Clock().tick(_fps)  # move frame by 1
    #DRAW TEST ROOM OBJECTS
    mainGame.gameDisplay.fill((255,255,255)) # fill the screen with white

    ##COLLISION
    hitBoxRect.center = player_.rect.center # this is a smaller box inside the player thats half the players size which will handle our logical collisions
##    pygame.draw.rect(mainGame.gameDisplay, (255,0,0),hitBoxRect) # debug 

    objs = pygame.sprite.groupcollide(entities2, soloEntity,False,False) # get all items colliding with player
    if len(objs) == 0 and not player_.isRising() or (BlockType.GROUND not in objs and not player_.isRising()):
        player_.State = Player.GState.FALLING

    for obj in objs: # iterate through all of them
        if obj.type == BlockType.GROUND: #if colliding with the ground
            if (hitBoxRect.bottom < obj.rect.center[1]) and player_.isFalling() or hitBoxRect.bottom + (player_.maxSpeedY * player_.y_acc) in range(obj.rect.top,obj.rect.center[1]):
                player_.State = Player.GState.GROUNDED # tell the game that player is standing on ground
                player_.y_acc = 0
                hitBoxRect.bottom = obj.rect.top
                player_.rect.center = (player_.rect.center[0],hitBoxRect.center[1]) # collision with ground added with a fourth of the players' height so he doesnt fall infinitely on the floor
        elif obj.type == BlockType.RIGHT_SLOPE and not player_.jumping:
            if player_.rect.center[0] in range(obj.rect.left, obj.rect.right) and player_.rect.center[1] > (obj.rect.bottom - (player_.rect.center[0] - obj.rect.left))-16: # if the player is below a certain point relative to the left side of the slope, it will lock him to that position
                player_.State = Player.GState.GROUNDED
                player_.y_acc = 0
                player_.x_acc /= 1.15
                hitBoxRect.bottom = obj.rect.bottom - (player_.rect.center[0] - obj.rect.left)
                player_.rect.center = player_.rect.center[0], hitBoxRect.center[1]
                break
        elif obj.type == BlockType.LEFT_SLOPE and not player_.jumping:
            if player_.rect.center[0] in range(obj.rect.left, obj.rect.right) and player_.rect.center[1] > (obj.rect.bottom - abs(player_.rect.center[0] - obj.rect.right))-16: # if the player is below a point relative to the right side of the slope, it will lock him to that position (absolute value because the players x-position is always less than the right side of the object)
                player_.State = Player.GState.GROUNDED
                player_.y_acc = 0
                player_.x_acc /= 1.15
                hitBoxRect.bottom = obj.rect.bottom - abs(player_.rect.center[0] - obj.rect.right)
                player_.rect.center = player_.rect.center[0], hitBoxRect.center[1]
                break
                        
        elif obj.type == BlockType.WALL: #if colliding with a wall
            if hitBoxRect.right > obj.rect.right: # approaching from the right moving left
                if player_.x_acc > 0: # getting off the wall, this needs to be here or else the player will remain stuck on walls until they fall off
                    player_.rect.left += 1
                else:
                    hitBoxRect.left = obj.rect.right # hitBoxRect will line up with the wall in a way that the player's model still collides but is not allowed to pass through (to avoid awkward bouncing off the wall)
                    player_.rect.center = (hitBoxRect.center[0],player_.rect.center[1])  
                    player_.x_acc = 0
                    player_.onWallLeft = True
            elif hitBoxRect.left < obj.rect.left: # approaching from the left moving right
                if player_.x_acc < 0: # getting off the wall, this needs to be here or else the player will remain stuck on walls until they fall off
                    player_.rect.left -= 1
                else:
                    hitBoxRect.right = obj.rect.left  # hitBoxRect will line up with the wall in a way that the player's model still collides but is not allowed to pass through (to avoid awkward bouncing off the wall)
                    player_.rect.center = (hitBoxRect.center[0], player_.rect.center[1]) 
                    player_.x_acc = 0
                    player_.onWallRight = True
        elif obj.type == BlockType.CEILING:
            if hitBoxRect.bottom > obj.rect.bottom and not player_.isFalling():
                hitBoxRect.top = obj.rect.bottom # hitBoxRect will line up with the wall in a way that the player's model still collides but is not allowed to pass through (to avoid awkward bouncing off the wall)
                player_.rect.center = (player_.rect.center[0], hitBoxRect.center[1])

        elif obj.type == BlockType.HYBRID:
            if player_.rect.center[0] in range(obj.rect.left, obj.rect.right):
                if hitBoxRect.bottom > obj.rect.top and hitBoxRect.bottom <= obj.rect.center[1]:
                    player_.State = Player.GState.GROUNDED # clearly the player isnt moving in air if the y-axis variables are 0
                    player_.y_acc = 0
                    hitBoxRect.bottom = obj.rect.top # hitBoxRect will line up with the wall in a way that the player's model still collides but is not allowed to pass through (to avoid awkward bouncing off the wall)
                    player_.rect.center = (player_.rect.center[0], hitBoxRect.center[1]+1) # collision with ground added with a fourth of the players' height so he doesnt fall infinitely on the floor
                elif (hitBoxRect.top <= obj.rect.bottom and hitBoxRect.center[1] > obj.rect.center[1])  and (hitBoxRect.center[0] in range(obj.rect.left,obj.rect.right)): # hitting the bottom of the hybrid blocks
                    hitBoxRect.top = obj.rect.bottom+1
                    player_.rect.center = (player_.rect.center[0], hitBoxRect.center[1]) # making player lock to the hitbox's position ensures that the player does not move since the hitbox does not update based on physics surrounding it

                    
            elif player_.rect.center[1] in range(obj.rect.top,obj.rect.bottom):
                if hitBoxRect.left > obj.rect.right: # approaching from the right moving left ; player's center point lines up with the wall vertically
                    if player_.x_acc > 0: # getting off the wall, this needs to be here or else the player will remain stuck on walls until they fall off
                        player_.rect.left += 1
                    else:
                        player_.rect.center = (hitBoxRect.center[0], player_.rect.center[1]) # making player lock to the hitbox's position ensures that the player does not move since the hitbox does not update based on physics surrounding it
                        player_.x_acc = 0
                        player_.onWallLeft = True
                elif hitBoxRect.right < obj.rect.left: # approaching from the left moving right ; player's center point lines up with the wall vertically
                    if player_.x_acc < 0: # getting off the wall, this needs to be here or else the player will remain stuck on walls until they fall off
                        player_.rect.left -= 1
                    else:
                        #hitBoxRect.right = obj.rect.left # hitBoxRect will line up with the wall in a way that the player's model still collides but is not allowed to pass through (to avoid awkward bouncing off the wall)
                        player_.rect.center = (hitBoxRect.center[0],player_.rect.center[1]) # hitBoxRect contains the last position of the player in the previous frame, therefore if we just make the player's position the last know position before colliding with the wall, there is no risk of getting stuck
                        player_.x_acc = 0
                        player_.onWallRight = True      

        elif obj.type == BlockType.SPECIAL:
            player_.resetBool = True
            levelCode += 1
            if levelCode % 5 == 0:
                mainGame.quitGame()
                print("Game complete! your time is: " + str(datetime.now()-startTime)[:-4])
            else:
                level_.drawLevel(levelCode % 5)

    #############################################
    #PRIMARY EVENT HANDLE BLOCK##################
    
    #PLAYER MOVEMENT
    '''Player movement comes first because we want to cancel any movement inputs when it comes to stuff like wall jumping'''
    keys = pygame.key.get_pressed() # gets movement keys pressed ; I learned that these do not need to be in the event handle block and that they do read buttons that are held down AS LONG AS THIS IS OUTSIDE OF ANY LOOP (like before, it was inside of the event for loop which broke its functionality)
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not player_.dashing: # if both are held down at the same time, player stops moving/doesnt move
        player_.decc_x = True
    elif keys[pygame.K_LEFT] and not player_.dashing: # move player left if left key is held
        player_.Face = Player.Facing.LEFT # (notice this one says Player instead of player_; the enumerators are constants that belong to the Player object, we want to avoid using the Enums inside of a player instance
        val = 0.1 if player_.isGrounded() else 0.05 # make sure the player cannot move as fast in the air as opposed to being grounded
        player_.x_acc = cap(-4, player_.x_acc - val) # I figured that we dont need to cap acceleration at +/-1 since speed is always capped anyway. Here, I cap it anyway since we dont want infinitely increasing numbers to appear anywhere in code
        player_.decc_x = False if player_.x_acc < 0 else True # helps in turning the player to make it feel like he isnt on ice
    elif keys[pygame.K_RIGHT] and not player_.dashing: # move player right if right key is held
        player_.Face = Player.Facing.RIGHT
        val = 0.1 if player_.isGrounded() else 0.05 # make sure the player cannot move as fast in the air as opposed to being grounded
        player_.x_acc = cap(4, player_.x_acc + val)
        player_.decc_x = False if player_.x_acc > 0 else True # helps in turning the player to make it feel like he isnt on ice
    elif not player_.dashing: # if no keys are held down and not dashing, deccelerate the player until he/she stops moving
        player_.decc_x = True
    if keys[RESET_POS]: # debug; set player to be at the top of the screen
        player_.rect.top=100
        player_.rect.left=400
    for event in pygame.event.get(): # this gets pygame specific events (pressed keys, closing window, etc) except for keys held down after initial press (idk why theres a difference)
        if event.type == pygame.QUIT: # when the player intentionally closes the program
            mainGame.quitGame()

        if event.type == pygame.KEYDOWN: # this no longer reads keys held down so non-primary movement keys should not go here
            if event.key == pygame.K_q:
                print("test print")
            if keys[pygame.K_DOWN] and (event.key == JUMP_KEY or event.key == ALT_JUMP_KEY):
                for obj in pygame.sprite.spritecollide(player_, entities2,False):
                    if obj.type == BlockType.GROUND:
                        player_.State = Player.GState.FALLING
                        player_.y_acc = 0.5
                        player_.rect.top += 10 # jump through the floor; comes before normal jump so the player doesnt jump instead

            elif event.key == JUMP_KEY or event.key == ALT_JUMP_KEY: # this is the basic jump jey
                if player_.isGrounded()and not player_.dashing: # normal jump
                    jumpSound.play()
                    player_.State = Player.GState.RISING
                    player_.y_acc = -player_.maxYAcc # set y acceleration to max negative value
                    player_.rect.bottom -= 2 # get player off the floor 1 pixel to avoid making him stuck
                elif player_.onWallRight:
                    jumpSound.play()
                    player_.dashing = False # our very first "tech" which is cancelling a dash with a wall jump. This refunds air dashing which can be used for dynamic wall climbing
                    player_.y_acc = -player_.maxYAcc
                    player_.x_acc = -3.5
                    player_.onWallLeft = player_.onWallRight = False
                    player_.Face = Player.Facing.LEFT
                elif player_.onWallLeft:
                    jumpSound.play()
                    player_.dashing = False
                    player_.y_acc = (-player_.maxYAcc)
                    player_.x_acc = 3.5
                    player_.onWallLeft = player_.onWallRight = False
                    player_.Face = Player.Facing.RIGHT
                elif (event.key == JUMP_KEY or event.key == ALT_JUMP_KEY) and player_.doubleJump and not (player_.dashing): # double jump ; player must not be grounded, not be dashing, and cannot have double jumped already since last touching the ground
                    jumpSound.play()
                    player_.doubleJump = False # cannot double jump again until grounded (the double jump is refunded in a different section of code)
                    player_.y_acc = -(player_.maxYAcc) # player jumps at the same height
             
            if (event.key == DASH_KEY or event.key == ALT_DASH_KEY) and not (player_.isGrounded() or player_.dashing):
                dashSound.play()
                player_.dashing = True # make it so that player is in a dashing state, this will block additional inputs until the player reaches the ground
                player_.decc_x = False # prevent the player from losing x-velocity so the dash is a constant movement until player reaches the ground
                player_.y_acc = (-player_.maxYAcc / 2) # player has a slight arc upwards upon dashing
                if player_.isFacingRight(): # send player right if facing right
                    player_.x_acc = 2
                else:                                   # send player left if facing left
                    player_.x_acc = -2  

    #END EVENT HANDLE BLOCK######################
    #############################################

    #OTHER
        
    #UPDATE SCREEN
##    hitBoxRect.center = player_.rect.center # this is a smaller box inside the player thats half the players size which will handle our logical collisions ; moved elsewhere in code
    player_.updateGState()
    
    entities2.update(mainGame.gameDisplay)
    entities2.draw(mainGame.gameDisplay)
    soloEntity.update(mainGame.gameDisplay)
    soloEntity.draw(mainGame.gameDisplay)
    

    #DEBUG
    ##POSITION
    mainGame.gameDisplay.blit(font.render("x_pos = " + str(player_.rect.left), 0, (0,0,0)),(5,fontSpace * 0))
    mainGame.gameDisplay.blit(font.render("y_pos = " + str(player_.rect.top), 0, (0,0,0)),(5,fontSpace * 1))
    ##VELOCITY
    mainGame.gameDisplay.blit(font.render("x_speed = " + str(cap(player_.maxSpeedX +3*player_.dashing,player_.maxSpeedX * player_.x_acc)), 0, (0,0,0)),(5,fontSpace * 2))
    mainGame.gameDisplay.blit(font.render("y_speed = " + str(cap(player_.maxSpeedY,player_.maxSpeedY * player_.y_acc)), 0, (0,0,0)),(5,fontSpace * 3))
    ##ACCELERATION
    mainGame.gameDisplay.blit(font.render("x_acceleration = " + str(player_.x_acc), 0, (0,0,0)),(5,fontSpace * 4))
    mainGame.gameDisplay.blit(font.render("y_acceleration = " + str(player_.y_acc), 0, (0,0,0)),(5,fontSpace * 5))
    ##STATES
    mainGame.gameDisplay.blit(font.render(str(player_.State), 0, (0,0,0)),(5,fontSpace * 6))
    mainGame.gameDisplay.blit(font.render(str(player_.Face), 0, (0,0,0)),(5,fontSpace * 7))
    ##CURSOR POSITION
    mainGame.gameDisplay.blit(font.render("Mouse Position: %s,%s"  %(int(pygame.mouse.get_pos()[0]/32),int(pygame.mouse.get_pos()[1]/32)), 0, (0,0,0)),(5,fontSpace * 8))
    #SPRITE INFORMATION
    mainGame.gameDisplay.blit(
        font.render("Sprite Info: frame:%s offset:%s"  % (player_.spriteFrame, player_.spriteOffset),
        0,
        (0,0,0)),
        (5,fontSpace * 9))

    #TIME
    mainGame.gameDisplay.blit(font.render(("Time -  %s"  % (datetime.now() - startTime))[:-4], 0, (0,0,0)),(900,fontSpace * 1)) # trim the last 4 characters because its useless microseconds that players do not care about
##    # Pretend this block doesnt exist but I wish to immortalize it for personal reasons
##    if timeSec - int(timeSec/60)*60 < 10 and int(timeSec/60) - int(timeSec/3600)*60 < 10:
##        mainGame.gameDisplay.blit(font.render("Time -  %s:0%s:0%s"  % (int(timeSec/3600), int(timeSec/60) - int(timeSec/3600)*60 , timeSec - int(timeSec/60)*60), 0, (0,0,0)),(900,0))
##    elif timeSec - int(timeSec/60)*60 < 10:
##        mainGame.gameDisplay.blit(font.render("Time -  %s:%s:0%s"  % (int(timeSec/3600), int(timeSec/60) - int(timeSec/3600)*60 , timeSec - int(timeSec/60)*60), 0, (0,0,0)),(900,0))
##    elif int(timeSec/60) - int(timeSec/3600)*60 < 10:
##        mainGame.gameDisplay.blit(font.render("Time -  %s:0%s:%s"  % (int(timeSec/3600), int(timeSec/60) - int(timeSec/3600)*60 , timeSec - int(timeSec/60)*60), 0, (0,0,0)),(900,0))
##    else:
##        mainGame.gameDisplay.blit(font.render("Time -  %s:%s:%s"  % (int(timeSec/3600), int(timeSec/60) - int(timeSec/3600)*60 , timeSec - int(timeSec/60)*60), 0, (0,0,0)),(900,0))



    #scrollCamera(player_)
    #mainGame.gameDisplay.blit(font.render("FPS: %s" % str(pygame.time.Clock().tick(60)), 0, (0,0,0)),(5,550))

    pygame.display.update() # show all images drawn to the screen

        
if mainGame.isCrashed():
    print("the game crashed! exiting")
del mainGame
input()

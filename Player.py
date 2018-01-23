import pygame
from pygame.locals import *
from enum import Enum

X = 0
Y = 1
groundPos = 450 # global temporary variable (useless once collision is implemented) ; might use this for a global death barrier (below screen)

def cap(maxVal, eq): # caps a value to prevent an equation from breaking said cap ; global function
    if abs(eq) > abs(maxVal):
        return maxVal
    return eq

class Player(pygame.sprite.Sprite):
    #Class Block
    class Facing(Enum): # player facing state ; player class
        LEFT = 0
        RIGHT = 1
    
    class GState(Enum): # player ground state ; player class
        GROUNDED = 0
        RISING = 1
        FALLING = 2
        SUSPENDED = 3 # ropes/ladders
    #Encapulation Block
    
    #PLAYER DRAWING
    imgName = "player"
    #SPRITE
    spriteSheetR = pygame.image.load(imgName + "/spritesheetR.png")
    spriteSheetL = pygame.image.load(imgName + "/spritesheetL.png")
    spriteSize = 32
    spriteOffset = 0
    spriteFrame = 0
    prevOffset = 0 # this will be used to determine if spriteFrame needs to be reset
    frameCount = 0 # counts how many frames have passed
    frameLimit = 20 # this will be used to determine if spriteFrame needs to be incremented (after this many frames)
    frameAdvance = True # kill me ; if true the frame should increment, else decrement

    #PLAYER MOVEMENT
    x_acc = 0 # default x-acceleration value ; player class ; global object inherited
    y_acc = 0 # default y-acceleration value ; player class ; global object inherited
    decc_x = False # default boolean value for whether the game should deccelerate the player on the x axis or not ; player class ; global object inherited
    dashing = False
    doubleJump = True
    onWallLeft = False
    onWallRight = False
    resetBool = False
    jumping = False # we need this to stop grounded collisions from trapping the player on the ground
    ##CONSTANTS##
    defXDecc = 1.05 # default x-decceleration value ; player class ; global object inheited
    defYAcc = 0.04 # default y-acceleration value ; player class ; global object inherited
    maxYAcc = 1 # maximum acceleration value for y_acceleration (defYAcc will be added to y_acc every frame until it reaches this value) ; player class ; global object inherited
    maxSpeedX = 3 # maximum x speed ; player class ; global object inherited
    maxSpeedY = 5 # maximum y speed ; player class ; global object inherited


    Face = Facing.RIGHT
    State = None
    #Init Block
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = x
        self.ypos = y
        self.xvel = cap(self.maxSpeedX, self.maxSpeedX * self.x_acc)
        self.yvel = cap(self.maxSpeedY, self.maxSpeedY * self.y_acc)
        self.rect = pygame.Rect([x,y,32,32])
        self.image = self.spriteSheetR.subsurface(Rect([self.spriteFrame * self.spriteSize, (self.spriteOffset * self.spriteSize), self.spriteSize, self.spriteSize]))
        
    #Method Block
    def update(self, screen):
        self.applyPhysics()
        self.updateFrameOffset()
        self.animate()
        self.drawPlayer()
        # X AXIS
        if self.x_acc < 0:
            self.rect.left += cap(-self.maxSpeedX - 3*self.dashing, int(self.maxSpeedX * self.x_acc))
        else:
            self.rect.left += cap(self.maxSpeedX + 3*self.dashing, int(self.maxSpeedX * self.x_acc))
        # Y AXIS
##        if self.getPos()[Y] + (self.getMaxSpeed()[Y] * self.getAcc()[Y]) > groundPos-6: # prevents the player from clipping through the "ground"
##            self.setState(Player.GState.GROUNDED) # clearly the player isnt moving in air if the y-axis variables are 0
##            self.setYPOS(groundPos-6) # pseudo collision with ground
##            self.setYACC(0)
##            self.rect.top = groundPos-6 # pseudo collision with ground
        if not self.isGrounded():
            self.rect.top += cap(self.maxSpeedY, int(self.maxSpeedY * self.y_acc))
        else:
            self.dashing = False # player cannot dash on ground, also cannot dash more than once in air
            self.doubleJump = True # refund double jump upon landing
        self.screenLoop(0,1024)
        if self.resetBool:
            self.reset(50,640)
        if self.rect.center[1] > 800:
            self.reset(50, 640)
            
    def updateFrameOffset(self):
        if abs(self.maxSpeedX * self.x_acc) > 0.5 or int(self.maxSpeedY * self.y_acc) != 0: # change which animation to display based on player X or Y speed (walking/ariel/standing/)
            if self.Face == self.Facing.LEFT:
                if self.State == self.GState.GROUNDED:
                    # walking left
                    self.spriteOffset = 10
                elif self.dashing:
                    self.spriteOffset = 11
                elif abs(self.y_acc) < 0.35: # if slowed in the air, there is a special frame that represents the player at the peak of a jump
                    self.spriteOffset = 8
                elif self.State == self.GState.RISING:
                    # rising left
                    self.spriteOffset = 7
                else:
                    # falling left
                    self.spriteOffset = 9
            else:
                if self.State == self.GState.GROUNDED:
                    # walking right
                    self.spriteOffset = 4
                elif self.dashing:
                    self.spriteOffset = 5
                elif abs(self.y_acc) < 0.35: # same special frame but for facing right
                    self.spriteOffset = 2
                elif self.State == self.GState.RISING:
                    # rising right
                    self.spriteOffset = 1
                else:
                    # falling right
                    self.spriteOffset = 3
                
        else: # player is not moving at all, just need to check which way he/she is facing to show the correct image
            if self.Face == self.Facing.LEFT and self.State == self.GState.GROUNDED:
                # standing facing left
                self.spriteOffset = 6
            elif self.Face == self.Facing.RIGHT and self.State == self.GState.GROUNDED:
                # standing facing right
                self.spriteOffset = 0

    def drawPlayer(self): # draw player at x position and y position ; player class
        if self.spriteOffset < 6:    
            self.image = self.spriteSheetR.subsurface(Rect([self.spriteFrame * self.spriteSize, (self.spriteOffset * self.spriteSize), self.spriteSize, self.spriteSize]))
        else:
            self.image = self.spriteSheetL.subsurface(Rect([self.spriteFrame * self.spriteSize, (self.spriteOffset - 6) * self.spriteSize, self.spriteSize, self.spriteSize]))

    def animate(self):
        if self.prevOffset != self.spriteOffset: # if the player has changed actions (i.e. started walking in the other direction)
            self.spriteFrame = 0 # reset animation frame
        if self.frameCount == self.frameLimit: # if the current animated frame has been displayed for $frameLimit frames, reset the counter and advance the animation frame
            self.frameCount = 0
            if self.isGrounded(): # currently only grounded states have multiple frames, all aerial frames are not animated so we avoid error with this catch
                if self.advanceFrame: # do not loop animation (increment frame)
                    self.spriteFrame = abs(self.spriteFrame + 1)
                else: # loop animation (decrement frame)
                    self.spriteFrame = abs(self.spriteFrame - 1)                    
                    
        if self.spriteFrame >= 2: # loop logic
            self.advanceFrame = False
        elif self.spriteFrame <= 0:
            self.advanceFrame = True
        self.frameCount += 1 # increment frame counter
        self.prevOffset = self.spriteOffset # store current offset value for the next time this function is called

    def screenLoop(self, minVal, maxVal): # this will ensure that the player loops around the screen when touching the sides
        if self.rect.center[0] > maxVal + 50: # we add 50 pixels to make the player model disappear completely on one side before looping around
            self.rect.left = minVal - 20
        elif self.rect.center[0] < minVal - 50:
            self.rect.left = maxVal + 10

    def updateGState(self):
        #PLAYER GROUND STATE
        if self.isGrounded():
            jumping = False
            return
        elif self.y_acc < 0:
            self.jumping = True
            self.State = Player.GState.RISING # if the acceleration variable is negative, the player is rising (I know this isnt how physics works but trust me on this)
        else:
            self.State = Player.GState.FALLING # if the acceleration variable is positive, the player is falling 
            self.jumping = False
            
    def applyPhysics(self):
        self.onWallLeft = self.onWallRight = False # reset these values, if the player is indeed touching a wall in the next frame the game will know before the event handle block
        if abs(float(self.x_acc)) < 0.001: # if acceleration falls below a low number, stop deccelerating and set it equal to 0 to save CPU
            self.x_acc = (0)
            self.decc_x = (False)
        if not self.isGrounded(): # apply gravity
            self.y_acc = cap(self.maxYAcc, (self.y_acc + self.defYAcc)) # acceleration is updated as the player falls (increased speed over time), acceleration and speed are capped
        self.x_acc = (self.deccPlayer()) # acceleration is updated based on the decceleration_x (decc_x) variable, if its false then it does not change

    def deccPlayer(self): # This checks if the game wants to deccelerate players movement, if yes then the acceleration value is divided by a constant and returned; physics class
        if self.decc_x:
            self.x_acc /= self.defXDecc
            return self.x_acc
        return self.x_acc

    def reset(self,x,y):
        self.rect.center = (x,y)
        self.resetBool = False
    def hitlag(self):
        return
    def attack(self):
        return
    def takeDamage(self):
        return      
    def isDecc(self):
        return self.decc_x
    def isGrounded(self):
        return self.State == self.GState.GROUNDED
    def isRising(self):
        return self.State == self.GState.RISING
    def isFalling(self):
        return self.State == self.GState.FALLING
    def isFacingLeft(self):
        return self.Face == self.Facing.LEFT
    def isFacingRight(self):
        return self.Face == self.Facing.RIGHT

#IMPORTANT NOTE: NEVER STACK HYBRID BLOCKS VERTICALLY; USE WALLS AND THEN PUT HYBRID BLOCKS ON EACH END
import pygame
from enum import Enum
[
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "W------------------------------W",
        "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH",
] # use this list as a base line for drawing any level
levels = ["",]

level = ["C"*32,
        "W"+("-"*30)+"X",
        "W"+("-"*5)+("H"*25)+"H", # hybrid block below special block is a must
        "W"+("-"*18)+("W")+("-"*11)+"W", 
        "W"+("-"*18)+("W")+("-"*11)+"W", 
        "W"+("-"*18)+("W")+("-"*11)+"W", 
        "W"+("-"*18)+("W")+("G"*5)+("H")+("-"*5)+"W", 
        "W"+("-"*18)+("W")+("-"*5)+("W")+("-"*5)+"W",   
        "W"+("-"*24)+("W")+("-"*5)+"W",
        "W"+("H"*24)+("W")+("-"*5)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*8)+("H"*22)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("H"*25)+("-"*5)+"W",  
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "W"+("-"*30)+"W",
        "G"*32] # this list draws the layout of the level using ascii characters which represent what block type to place at (x*32,y*32) ; 32 is the size of the block
levels.append(level)

level = [
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W------------------------------W",
        "W----------------SH---H--------W",
        "W---------------SNW---W--HHHHHHW",
        "WS-------------SNNW---W--W-----X",
        "WNS-----------SNNNW---W--WGHHHHW",
        "WNNS---------SNNNNW---W--W-----W",
        "WNNNS-------SNNNNNW---W--W-----W",
        "WHHHHHHHHHHHHNNNNNW---W--W-----W",
        "W-----------WNNNNNW---W--W-----W",
        "W-----H-----WNNNNNW---W--W-----W",
        "W-----W-----WNNNNNW---W--W-GGG-W",
        "W-----W-----WNNNNNW---W--W-----W",
        "W-----W-----WNNNNNH---W--W-----W",
        "W-----W-----WNNNNNNNNNW--W-----W",
        "W-----W-----WNNNNNNNNNW--W-----W",
        "W-----W-----WNNNNNNNNNW--WHHHH-W",
        "W-----W-----WNNNNNH---W--W-----W",
        "W-----W-----HNNNNNW---W--W-----W",
        "W-----W-----NNNNNNH---W--W-----W",
        "W-----W-----NNNNNNN---W--W-----W",
        "W-----W-----HHNNNNN---W--------W",
        "W-----W-----NNNNNNN---W--------W",
        "WHHH--------NNNNNNN---W--------W",
]

levels.append(level)

level = [
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W------------------------------W",
        "W--------GGGGH---------HHHHHHH-W",
        "W------------W---------------W-W",
        "W------------W---------------W-W",
        "W------------H---------------W-W",
        "W----H-----------------------W-W",
        "W----W-----------------------W-W",
        "W----W-----------------------W-W",
        "W----W---H-------------------W-W",
        "W----H---W-------------------W-W",
        "W--------W-------------------W-W",
        "W--------H-------------------W-W",
        "W----------------------------W-W",
        "W----GGG---------------------W-W",
        "W----------------------------W-W",
        "W---H------------------------W-W",
        "W---W------------------------W-W",
        "W---W--------------------HHHHH-W",
        "W---W--------------------W-----W",
        "W---H--------------------W-----W",
        "W------------------------W-----W",
        "W------------------------WX----W",
        "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"

]

levels.append(level)

level = [
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W------------------------------W",
        "W-----HHHHHHHHHHHHHHHHHHHHH---HW",
        "W-GGG-W------------------------W",
        "W-----W---GG------G-------GGHHHW",
        "WG---GW------------------------W",
        "W-GGG-WGG----------------------W",
        "W-----W------------------------W",
        "WG---GW------------------------W",
        "W-----W------------------------W",
        "W-GGG-W-HHH----HHH-----HHH-----W",
        "W-----W-----------------------HW",
        "WG---GW------------------------W",
        "W-----W--------------------GG--W",
        "W-GGG-W------------------------W",
        "W-----W------------------------W",
        "WHHHHGW---------HHHH-----HHHHHHW",
        "X-----W--GGG-------------------W",
        "WHHHHHW------------------------W",
        "W-----W------------------------W",
        "W-----W------------------------W",
        "W-----HHHHHHHHHHHHHHHHHHHHHHH--W",
        "W------------------------------W",
        "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
]

levels.append(level)

class BlockType(Enum):
    GROUND = 0
    WALL = 1
    CEILING = 2
    HYBRID = 3
    SPECIAL = 4
    NULL = 5 # mostly for scenery; no collision properties
    RIGHT_SLOPE = 6
    LEFT_SLOPE = 7
    
class Block(pygame.sprite.Sprite): # primarily individual blocks to be drawn on the screen with special properties
    def __init__(self, rect, name, type_, color=(150,150,150), active=True):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((rect.width,rect.height)) # create a surface on top of the object with its dimensions which will represent how it will be drawn on the screen
        self.color = color
        self.name = name # name of block; usually just has the coordinates of its top-left corner
        self.type = self.trueType = type_ # trueType stores the value of passed type_ in case the object is rendered inactive in which the type changes to null
        self.active = active # this will determine if the object should be drawn and have collision properties [OUTDATED]
        self.deactivated = False
        if self.type == BlockType.RIGHT_SLOPE:
            self.image.fill((255,255,255))
            for point in range(0, rect.width):
                pygame.draw.line(self.image, color, (point, rect.height), (point, rect.width - point)) # draw lines from bottom-up, left to right with increasing height like a forward slash --> /
        elif self.type == BlockType.LEFT_SLOPE:
            self.image.fill((255,255,255))
            for point in range(0, rect.width):
                pygame.draw.line(self.image, color, (point, point), (point, rect.height)) # draw lines from top-bottom, left to right each starting at a lower position like a back slash --> \
        else:
            self.image.fill(color) # draw the block with a given color (grey of none passed)

    def __repr__(self):
        return self.type

    
    def update(self, screen): # ignore everything in this function it is useless and outdated 
        if not self.active and not self.deactivated:
            self.deactivated = True 
            self.image.fill((255,255,255))
            self.type = BlockType.NULL # TODO: change this; NULL Block objects should be drawn to the screen just not have collision
        if pygame.Rect((pygame.mouse.get_pos()), (1,1)).colliderect(self.rect) and not self.active:
            self.deactivated = False
            self.image.fill((100,100,100))
            if pygame.mouse.get_pressed()[0]:
                print(self.name)
                self.active = True
                self.type = self.trueType
                self.image.fill(self.color)
                print(self.type)
        elif pygame.Rect((pygame.mouse.get_pos()), (1,1)).colliderect(self.rect):
            if pygame.mouse.get_pressed()[2]:
                print(self.name)
                self.active = False
      
        return

class Level: # container of Block objects
    def __init__(self, code, sprGroup):
        self.code = code # level code (i.e. level 1, 2, 3...)
        self.sprGroup = sprGroup # pygame exclusive; required to draw things to the screen
        if code == -1: # if the object is called with -1, doesnt immediately draw a level (can be used for a menu or something)
            return
        else:
            self.drawLevel(code) # draw the Block blocks
    def drawLevel(self, code):
        self.code = code
        for itm in self.sprGroup.sprites(): # clear the previous group of blocks for the new set (like an etch-a-sketch)
            del itm # free memory
        self.sprGroup.empty() # final clear (this doubles down on clearing the sprites, it isnt really necessary)
        self.level = levels[self.code] # get the new level list to process
        '''
        The way levels are handled in this code is it takes a 32x24 list of strings and goes through each string character-by-character.
        Depending on what the character is, the game will draw an Block block of that type (i.e. 'H' = Hybrid block type)
        This list of strings visually represents what the level would look like
        '''
        for y in range(0,24):
            for x in range(0,32):
                envType = self.level[y][x]
                if envType == "H":
                    self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.HYBRID))
                elif envType == "G":
                    self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,16),"block (%s,%s)" % (x,y), BlockType.GROUND))
                elif envType == "W":
                    self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.WALL))
                elif envType == "C":
                    self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.CEILING))                    
                elif envType == "X": # SPECIAL BLOCK
                    self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.SPECIAL, (255,0,0)))
                elif envType == "N":
                    self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.NULL, (50,50,50)))
                elif envType == "S":
                    #TODO : perform checks to determine if there should be a left slope or right slope
                    if x != 0 and self.level[y][x-1] == "-": # if index is not zero (to avoid out of range error from x-1) and there is no block to the left of this block
                        self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.RIGHT_SLOPE, (0,100,0))) # draw a left-sided slope
                    else:
                        self.sprGroup.add(Block(pygame.Rect(x*32,y*32,32,32),"block (%s,%s)" % (x,y), BlockType.LEFT_SLOPE, (0,100,0))) # draw a right-sided slope
                        
